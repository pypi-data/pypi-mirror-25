import logging
import itertools
import copy

import jq
import jsonpointer


import yadage.handlers.utils as utils
from .expression_handlers import handlers as exprhandlers
from ..tasks import packtivity_task, init_task, outputReference
from ..stages import JsonStage
from ..utils import leaf_iterator_jsonlike, pointerize


log = logging.getLogger(__name__)

handlers, scheduler = utils.handler_decorator()

# A scheduler does the following things:
#   - attached new nodes to the DAG
# - for each added step
#     - the step is given a name
#     - the step parameters are determined using the scheduler spec and context
#     - a list of used inputs (in the form of [stepname,outputkey,index])

def select_parameter(wflowview, parameter):
    '''
    Evaluates parameter expressions (if needed) in the context of a workflow view

    :param wflowview: the workflow view on which to evaluete possible value expressions
    :param parameter: either a non-dict value or a JSON-like dict for a
                      supported value expression
    :return: the parameter value 
    '''
    if type(parameter) is not dict:
        value = parameter
    else:
        handler = exprhandlers[parameter['expression_type']]
        value = handler(wflowview, parameter)
    return value

def finalize_value(wflowview, step, value, state):
    '''
    finalize a value by recursively resolving references and
    contextualizing it for the passed state context

    :param wflowview: the workflow view against which to resolve upstream references
    :param step: the step for which to track usage of upstream references
    :param value: the parameter value. May be a output reference, or a JSON value type
    :param state: the state context used to contextualize parameter values
    :return: finalized parameter value
    '''
    if type(value) == outputReference:
        step.used_input(value)
        v = value.pointer.resolve(wflowview.dag.getNode(value.stepid).result)
        return finalize_value(wflowview, step, v, state)
    if state:
        return state.contextualize_data(value)
    else:
        return value


def finalize_input(wflowview, step, jsondata):
    '''
    evaluate final values of step parameters by resolving 
    references to a upstream output and contextualizing stateful
    parameters. Also tracks usage of upstream references for the step

    :param wflowview: the workflow view view against which to resolve any upstream references
    :param step: the step that for which to track usage of upstream references
    :param jsondata: the prospective step parameters

    :return: finalized step parameters
    '''

    state =  step.state if hasattr(step, 'state') else None
    result = copy.deepcopy(jsondata)
    for leaf_pointer, leaf_value in leaf_iterator_jsonlike(jsondata):
        leaf_pointer.set(result,finalize_value(wflowview, step, leaf_value, state))
    return result

def step_or_init(name, spec, state_provider):
    '''
    create a named packtivity_task of sub-workflow init_task object based on stage spec

    :param name: name of the eventual (init-)step
    :param spec: the stage spec
    :param state_provider: the stage's state provider

    :return: yadage or init step object
    '''
    if 'step' in spec:
        step_state = state_provider.new_state(name)
        return packtivity_task(name=name, spec=spec['step'], state=step_state)
    elif 'workflow' in spec:
        return init_task('init {}'.format(name))
    raise RuntimeError('do not know what kind of stage spec we are dealing with.')

def addStepOrWorkflow(name, stage, step, spec):
    '''
    adds a step or a sub-workflow belonging to a stage this stage init step to the current workflow view
    
    :param str name: the name of the step or sub-workflow
    :param stage: the stage from which to use state context and workflow view
    :param step: either a packtivity_task (for normal workflow steps) initstep object (for sub-workflows)
    :param spec: the stage spec

    :return: None
    '''
    if type(step) == init_task:
        new_provider = stage.state_provider.new_provider(name)
        subrules = [JsonStage(yml, new_provider) for yml in spec['workflow']['stages']]
        stage.addWorkflow(subrules, initstep=step)
    else:
        stage.addStep(step)

def get_parameters(spec):
    '''
    retrieve parameters from the spec

    :param spec: the stage spec
    :return: a JSON-like object of stage parameters
    '''
    return {x['key']: x['value']for x in spec['parameters']}

@scheduler('singlestep-stage')
def singlestep_stage(stage, spec):
    '''
    a simple state that adds a single step/workflow. The node is attached
    to the DAG based on used upstream outputs
    
    :param stage: common stage parent object 
    :param spec: stage JSON-like spec
    
    :return: None
    '''
    log.debug('scheduling singlestep stage with spec:\n%s', spec)

    step = step_or_init(stage.name,spec,stage.state_provider)

    parameters = {
        k: select_parameter(stage.view, v) for k, v in get_parameters(spec).items()
    }

    finalized = finalize_input(stage.view, step, parameters)
    addStepOrWorkflow(stage.name, stage, step.s(**finalized), spec)


def chunk(alist, chunksize):
    '''split a list into equal-sized chunks of size chunksize'''
    return [alist[x:x+chunksize] for x in range(0, len(alist), chunksize)]


def partition(alist, partitionsize):
    '''split a list into partitionsize parts'''
    total_len = len(alist)
    if partitionsize > total_len:
        partitionsize = total_len
    assert partitionsize <= total_len
    end = 0 
    partitioned = []
    for k in range(partitionsize):
        begin = end
        end =  end + (total_len+k)//partitionsize
        partitioned.append(alist[begin:end])
    return partitioned

def groupmany(iterable,batchsize = None, partitionsize = None):
    if batchsize:
        return chunk(list(iterable), batchsize)
    if partitionsize:
        return partition(list(iterable), partitionsize)
    return iterable


def scatter(parameters, scatter, batchsize = None, partitionsize = None):
    '''
    convert a parameter set and scatter definition into a list
    of single parameter sets.

    :param parameters: the parameter definition
    :param scatter: scattering method. One of 'zip' or 'cartesian'

    :return: list of parameter sets
    '''

    commonpars = parameters.copy()
    to_scatter = {}
    for scatpar in scatter['parameters']:
        to_scatter[scatpar] = groupmany(commonpars.pop(scatpar), batchsize, partitionsize)

    singlesteppars = []
    if scatter['method'] == 'zip':
        keys, zippable = zip(*[(k, v) for k, v in to_scatter.items()])


        for zipped in zip(*zippable):
            individualpars = dict(zip(keys, zipped))
            pars = commonpars.copy()
            pars.update(**individualpars)
            singlesteppars += [pars]

    if scatter['method'] == 'cartesian':
        for what in itertools.product(*[to_scatter[k] for k in scatter['parameters']]):
            individualpars = dict(zip(scatter['parameters'], what))
            pars = commonpars.copy()
            pars.update(**individualpars)
            singlesteppars += [pars]
    return singlesteppars


@scheduler('multistep-stage')
def multistep_stage(stage, spec):
    '''
    a stage that attaches an array of nodes to the DAG. The number of nodes
    is determined by a scattering recipe. Currently two algs are supported

    - ``zip``: one or more arrays of length n are iterated through in lock-step.
       n nodes are added to the DAG where the  parameters values are set to
           the values in the iteration
    - ``cartesian``:  a cartesian product of a number of arrays (possibly different sizes)
       adds n1 x n2 x ... nj nodes.

    Nodes are attached to the DAG based on used upstream inputs

    :param stage: common stage parent object 
    :param spec: stage JSON-like spec
    
    :return: None
    '''
    log.debug('scheduling multistep stage with spec:\n%s', spec)
    parameters = {
        k: select_parameter(stage.view, v) for k, v in get_parameters(spec).items()
    }
    singlesteppars = scatter(parameters, spec['scatter'], spec.get('batchsize'), spec.get('partitionsize'))
    for i, pars in enumerate(singlesteppars):
        singlename = '{}_{}'.format(stage.name, i)
        step = step_or_init(singlename,spec,stage.state_provider)
        finalized = finalize_input(stage.view, step, pars)
        addStepOrWorkflow(singlename, stage, step.s(**finalized), spec)


@scheduler('jq-stage')
def jq_stage(stage, spec):
    '''

    :param stage: common stage parent object 
    :param spec: stage JSON-like spec
    
    :return: None
    '''

    binds = spec['bindings']
    wflowrefs = [jsonpointer.JsonPointer.from_parts(x) for x in jq.jq('paths(if objects then has("$wflowref") else false end)').transform(binds, multiple_output = True)]

    for wflowref in wflowrefs:
        nodeselector, resultscript = wflowref.resolve(binds)['$wflowref']
        view = stage.view
        nodestruct = jq.jq(nodeselector).transform(view.steps, multiple_output = True)

        noderefs = [jsonpointer.JsonPointer.from_parts(x) for x in jq.jq('paths(if objects then has("_nodeid") else false end)').transform(nodestruct, multiple_output = True)]
        for nr in noderefs:
            n = view.dag.getNode(nr.resolve(nodestruct)['_nodeid'])
            r = jq.jq(resultscript).transform(pointerize(n.result,False,n.identifier), multiple_output = True)
            nr.set(nodestruct,r)
        wflowref.set(binds,nodestruct)

    log.info('transforming binds: %s', binds)
    stagescript = spec['stepscript']
    stageres = jq.jq(stagescript).transform(binds,multiple_output = False)

    singlesteppars = []
    for forstep in stageres:
        wflowpointers = [jsonpointer.JsonPointer.from_parts(x) for x in jq.jq('paths(if objects then has("$wflowpointer") else false end)').transform(forstep, multiple_output = True)]
        for wflowptr in wflowpointers:
            pointer =  wflowptr.resolve(forstep)['$wflowpointer']
            wflowptr.set(forstep,outputReference(pointer['step'],jsonpointer.JsonPointer(pointer['result'])))
        singlesteppars.append(forstep)
        log.info(forstep)

    postscript = spec['postscript']
    for i, pars in enumerate(singlesteppars):
        singlename = '{}_{}'.format(stage.name, i)
        step = step_or_init(singlename,spec,stage.state_provider)
        finalized = finalize_input(stage.view, step, pars)

        log.info('postscripting: %s',finalized)
        after_post = jq.jq(postscript).transform(finalized,multiple_output = False)

        log.info('finalized to: %s',after_post)
        addStepOrWorkflow(singlename, stage, step.s(**after_post), spec)



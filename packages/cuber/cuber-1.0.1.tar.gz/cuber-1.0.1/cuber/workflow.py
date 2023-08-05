import importlib
import copy
import json
import commentjson
import logging
from functools32 import lru_cache
import traceback
import utils

logger = logging.getLogger(__name__)

class Workflow():
    def __init__(self, workflow_file = None, graph = None, main = 'main', graph_args = {}):
        '''
        Example:
        {
            'module': 'dcg_metric',
            'class': 'DCGMetric',
            'deps': [
                {
                    'prefix': 'model1',
                    'graph': {

                    }
                },
                {
                    'arg_name': 'data',
                    'graph': {
                        'module': 'lastfm_data',
                        'class': 'LastFMData',
                        'attrs': {
                            'short': False,
                        }
                    }
                }

            ]
        }
        '''
        self.graph_args = graph_args
        self.main = main
        if workflow_file is not None:
            with open(workflow_file) as f:
                graph_json = f.read()
            logger.debug('Graph json: {}'.format(graph_json))
            self.graph = commentjson.loads(graph_json)
        elif isinstance(graph, basestring):
            graph_json = graph
            logger.debug('Graph json: {}'.format(graph_json))
            self.graph = commentjson.loads(graph_json)
        else:
            self.graph = graph
        logger.debug('Graph args: {}'.format(graph_args))

    def get_graph(self, name):
        return self.graph[name]

    def __substitute_graph_args(self, attrs):
        attrs_ = {}
        for key, value in attrs.iteritems():
            if isinstance(value, basestring) and value.startswith('$'):
                graph_args_key = value[1:]
                logger.debug('Substitute param: {}'.format(graph_args_key))
                if graph_args_key not in self.graph_args:
                    raise ValueError('Key {} is not specified in graph args: {}'.format(graph_args_key, self.graph_args))
                attrs_[key] = self.graph_args[graph_args_key] 
            else:
                attrs_[key] = value
        return attrs_

    def run(self, disable_inmemory_cache = False, disable_file_cache = False):
        return self.__run_graph(self.main, disable_inmemory_cache = disable_inmemory_cache, disable_file_cache = disable_file_cache)

    def __run_graph(self, graph_, disable_inmemory_cache, disable_file_cache):
        '''
            TODO: improve excprions for incorrect graph
        '''
        logger.info('Graph to do: {}'.format(graph_))

        if isinstance(graph_, basestring): # this is graph name
            logger.info('Go to {}'.format(graph_))
            return self.__run_graph(self.get_graph(graph_), disable_inmemory_cache = disable_inmemory_cache, disable_file_cache = disable_file_cache)

        # required fields
        for key in {'module', 'class'}:
            assert key in graph_

        for key in graph_.keys():
            assert key in {'attrs', 'deps', 'class', 'module', 'comment', 'disable_inmemory_cache', 'disable_file_cache'}

        attrs = copy.deepcopy(graph_.get('attrs', {}))
        attrs = self.__substitute_graph_args(attrs)
        for dep in graph_.get('deps', {}):
            for key in dep.keys():
                assert key in {'fields', 'graph', 'prefix', 'comment'}

            res = self.__run_graph(dep['graph'], disable_inmemory_cache = disable_inmemory_cache, disable_file_cache = disable_file_cache)
            if 'fields' not in dep:
                for key in res:
                    attr_key = dep.get('prefix', '') + key
                    if attr_key in attrs:
                        logger.error('Parameter for cube is not unique: {} at graph:\n{}'.format(attr_key, graph_))
                        raise ValueError('Graph configuration error')
                    attrs[attr_key] = res[key]
            else:
                for new_key, old_key in dep['fields'].iteritems():
                    attr_key = dep.get('prefix', '') + new_key
                    if attr_key in attrs:
                        logger.error('Parameter for cube is not unique: {} at graph:\n{}'.format(attr_key, graph_))
                        raise ValueError('Graph configuration error')
                    attrs[attr_key] = res[old_key]

        module = importlib.import_module(graph_['module'])
        logger.debug('Attrs keys: {}'.format(attrs.keys()))
        try:
            cube_init = getattr(module, graph_['class'])(**attrs)
        except Exception as e:
            logging.error('Faild to init cube:\nCube: {cube}\nGraph part: {graph_part}\nAttrs: {attrs}\nError: {error}\nTraceback: {tb}' \
                .format(
                    cube = graph_['module'],
                    graph_part = str(graph_),
                    attrs = utils.dict_to_string(attrs, brackets = True),
                    error = str(e),
                    tb = traceback.format_exc(),
                )
            )
            raise

        try:
            res = cube_init.get(
                disable_inmemory_cache = disable_inmemory_cache or utils.parse_bool(graph_.get('disable_inmemory_cache', 'false')), 
                disable_file_cache = disable_file_cache or utils.parse_bool(graph_.get('disable_file_cache', 'false')),
            )
        except Exception as e:
            logging.error('Faild to cube.get():\nCube: {cube}\nGraph part: {graph_part}\nAttrs: {attrs}\nError: {error}\nTraceback: {tb}' \
                .format(
                    cube = graph_['module'],
                    graph_part = str(graph_),
                    attrs = utils.dict_to_string(attrs, brackets = True),
                    error = str(e),
                    tb = traceback.format_exc(),
                )
            )
            raise
        return res

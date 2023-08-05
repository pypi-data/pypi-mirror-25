import abc
import cPickle as pickle
import os.path
import logging

import cache

logger = logging.getLogger(__name__)

class Cube(object):
    __metaclass__  = abc.ABCMeta

    checkpoints_dir = 'checkpoints/'

    @abc.abstractmethod
    def name(self):
        '''
            Unique name for cube and params. This name is key for cache.
        '''
        return

    def get(self, disable_file_cache = False, disable_inmemory_cache = False, cleanup = False):
        '''
            Checks if there is a cached verison and loads it.
            If there is no cached version, runs calcualtions via eval function.
            If you want to get cube's result, use only this function.
        '''
        key = self.name() # hashing make take some time
        logger.debug('Key: {}'.format(key))

        data = None
        data_done = False # flag the data is already got from cache
        
        # resources the data is already uploaded to
        data_inmemory_cache = False
        data_file_cache = False

        # try load form memory
        if not disable_inmemory_cache and not data_done:
            cached, cached_data = cache.Cache().get(key)
            if cached: # true, if object is found 
                logger.debug('Loaded from in-memory cache')
                data = cached_data
                data_inmemory_cache = True
                data_done = True

        # try load from file
        pickle_name = os.path.join(Cube.checkpoints_dir, '{}.pkl'.format(key))
        if not disable_file_cache and not data_done:
            logger.info('Pickle name: {}'.format(pickle_name))
            if os.path.isfile(pickle_name):
                logger.debug('Loading from file cache')
                with open(pickle_name, 'rb') as f:
                    data = pickle.load(f)
                data_file_cache = True
                data_done = True

        if not data_done:
            logger.info('Caches do not contain the data. Evaluating...')
            data = self.eval()
            logger.info('Evaluated...')
            data_done = True

        # save to file cache
        if not disable_file_cache and not data_file_cache:
            logger.debug('Save to file cache')
            if not os.path.isdir(Cube.checkpoints_dir):
                os.makedirs(Cube.checkpoints_dir)
            with open(pickle_name, 'wb') as f:
                pickle.dump(data, f)

        if cleanup:
            if os.path.isfile(pickle_name):
                os.remove(pickle_name)

        # save to inmemory cache
        if not disable_inmemory_cache and not data_inmemory_cache:
            logger.debug('Save to inmemory cache')
            cache.Cache().add(key, data)

        return data

    @abc.abstractmethod
    def eval(self):
        '''
            This method should contain meaningful calculations. It have to return dict with result.
        '''
        return

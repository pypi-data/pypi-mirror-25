import json
import os
import shutil
import time
import random

from . import _config
from . import _db
from . import _downloads
from . import _helpers
import urllib.parse


class Dataset(object):
    def __init__(self, dataset_title):
        dataset_api_url = urllib.parse.urljoin(_config.API_URL, dataset_title)
        try:
            meta_data = _downloads.load_json_from_url(dataset_api_url)
        except:
            raise Exception('Can\'t connect to API server')

        if meta_data is not None:
            self.title = meta_data.get('title')
            self._archive_hash = meta_data.get('hash')
            self._url = meta_data.get('url')
            self._batch_size = _config.BATCH_SIZE
            self._size = meta_data.get('size')
            self.features = meta_data.get('features')
            self.index = 0
            self._error_count = 0
            self._middleware = None
        else:
            raise Exception('Dataset does not exist')

        self._dataset_dir = _downloads.maybe_download_and_extract(self._url, self.title, self._archive_hash)
        self._data_path = os.path.join(self._dataset_dir, _config.DATA_FILE_NAME)
        self._use_json = (os.path.getsize(self._data_path) < 1024 * 1024 * _config.MAX_INMEMORY_FILE_SIZE)
        self._data = None

        if meta_data.get('extra_data_files') is not None:
            extra_data_paths = map(lambda x: os.path.join(self._dataset_dir, x), meta_data.get('extra_data_files'))
            self.extra_data = _helpers.open_extra_data_files(extra_data_paths)
        else:
            self.extra_data = None

        if _config.MONGO_DB is not None:
            self._db = _config.MONGO_DB[self.title]

            if self._db.count() == 0:
                indices = _db.import_json_to_db(self._data_path, self._db)
                if len(indices) != self._size:
                    self._clear()
                    raise Exception('Dataset have unexpected size: {} (expected: {})'.format(len(indices), self._size))

            elif self._db.count() != self._size:
                self._db.drop()
                indices = _db.import_json_to_db(self._data_path, self._db)
                if len(indices) != self._size:
                    self._clear()
                    raise Exception('Dataset have unexpected size: {} (expected: {})'.format(len(indices), self._size))

            self._indices = random.sample(range(self._size), self._size)
            self._db_indices = _db.get_indices_from_db(self._db)
            random.shuffle(self._db_indices)

            self._source_type = 'db'
        else:
            self._indices = random.sample(range(self._size), self._size)
            self._source_type = 'json'
            self._db = None
            self._db_indices = None

    def get(self, batch_size=None):
        current_batch_size = batch_size if batch_size is not None else self._batch_size

        if current_batch_size > self._size:
            raise Exception('batch_size cannot be larger than dataset size')

        data = self._get_from_source(self.index, current_batch_size)

        self.index = self.index + current_batch_size

        if self.index >= self._size:
            self.index = self.index % self._size
            data += self._get_from_source(0, self.index)

        if self._middleware is not None:
            return self._middleware(data)
        else:
            return data

    def get_all(self):
        return self.get(self._size)

    def _get_from_source(self, initial_index, size):
        if self._source_type == 'db':
            while True:
                try:
                    return self._get_from_db(initial_index, size)
                except:
                    if self._use_json:
                        print("Can't access database, use json")
                        return self._get_from_json(initial_index, size)
                    else:
                        print("Can't access database")
                        wait_time = min(1 * 2 ** self._error_count, _config.MAX_AWAIT_TIME)
                        print('waiting for {} seconds'.format(wait_time))
                        time.sleep(wait_time)
                        self._error_count += 1
        else:
            return self._get_from_json(initial_index, size)

    def _get_from_json(self, initial_index, size):
        if self._data is None:
            with open(self._data_path) as f:
                self._data = json.load(f)
        indices = self._indices[initial_index:initial_index + size]
        return [self._data[i] for i in indices]

    def _get_from_db(self, initial_index, size):
        return list(
            self._db.find({"_id": {"$in": self._db_indices[initial_index:initial_index + size]}}, {'_id': False}))

    def _clear(self):
        shutil.rmtree(self._dataset_dir)

    def set(self, batch_size=None):
        if batch_size is not None:
            if batch_size > self._size:
                raise Exception('batch_size cannot be larger than dataset')
            if batch_size < 1:
                raise Exception('batch_size cannot be < 1')
            self._batch_size = batch_size
        return self

    def middleware(self, middleware):
        self._middleware = middleware
        return self

    def get_info(self):
        return {
            'title': self.title,
            'indices': self._indices,
            'db_indices': self._db_indices,
            'middleware': self._middleware,
            'batch_size': self._batch_size,
            'size': self._size,
            'directory': self._dataset_dir
        }

    def split(self, train_part, test_part):
        divider = (self._size * train_part) // (test_part + train_part)
        return PartialDataset(self.get_info()), PartialDataset(self.get_info())


class PartialDataset(Dataset):
    def __init__(self, copy):
        Dataset.__init__(self, copy.get('title'))
        self._indices = copy.get('indices')
        self._size = copy.get('size')
        self._middleware = copy.get('middleware')
        self._batch_size = copy.get('batch_size')
        self._db_indices = copy.get('db_indices')

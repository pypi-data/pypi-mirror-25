import datetime
import json
import logging
import sys
from functools import wraps
from threading import Thread

import six
from dateutil.parser import parse as parse_date


def attrs_to_dir(mod):
    data = {}
    for attr in dir(mod):
        if attr == attr.upper():
            data[attr] = getattr(mod, attr)
    return data


class Task(Thread):
    """
    The Threaded object returned by the @threaded decorator below
    """

    def __init__(self, method, *args, **kwargs):
        super(Task, self).__init__()
        self.method = method
        self.name = 'ETCDConfigThread'
        self.args = args
        self.kwargs = kwargs
        self._result = None
        self.__exc_info = None

    def run(self):
        try:
            self._result = self.method(*self.args, **self.kwargs)
        except:
            self.__exc_info = sys.exc_info()

    @property
    def result(self):
        self.join()
        if self.__exc_info is not None:
            six.reraise(*self.__exc_info)
        return self._result


def threaded(function=None, daemon=False):

    def wrapper_factory(func):

        @wraps(func)
        def get_thread(*args, **kwargs):
            t = Task(func, *args, **kwargs)
            if daemon:
                t.daemon = True
            t.start()
            return t

        return get_thread

    if function:
        return wrapper_factory(function)
    else:
        return wrapper_factory


class CustomJSONEncoder(json.JSONEncoder):

    custom_type_key = '_custom_type'
    custom_type_value_key = 'value'
    DECODERS = {'datetime': parse_date}

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return {self.custom_type_key: 'datetime',
                    self.custom_type_value_key: obj.isoformat()}
        else:
            return super(CustomJSONEncoder, self).default(obj)


def custom_json_decoder_hook(obj):

    ct = obj.get(CustomJSONEncoder.custom_type_key, None)
    if ct is not None:
        value = obj.get(CustomJSONEncoder.custom_type_value_key)
        return CustomJSONEncoder.DECODERS[ct](value)
    else:
        return obj


def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.items()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif (sys.version_info.major == 2) and (isinstance(input, unicode)):
        return input.encode('utf-8')
    else:
        return input


class IgnoreMaxEtcdRetries(logging.Filter):
    """
    Skip etcd.client MaxRetryError on timeout
    """

    def __init__(self, name='etcd.client'):
        super(IgnoreMaxEtcdRetries, self).__init__(name)

    def filter(self, record):
        msg = '{}'.format(record.args)
        return not (
            'MaxRetryError' in msg and
            'Read timed out' in msg
        )

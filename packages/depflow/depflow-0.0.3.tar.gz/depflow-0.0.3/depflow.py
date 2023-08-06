import logging
import os
import time
import random
from hashlib import md5
import json
import sqlite3
import re

logger = logging.getLogger('depflow')

_db_name = os.environ.get('DEPFLOW_CACHE', '.depflow.sqlite3')
_db = sqlite3.connect(_db_name)
logger.debug('Using cache at {}'.format(os.path.abspath(_db_name)))
_db.execute('create table if not exists keyvalue (key text primary key, value text not null)')  # noqa
_db.commit()

_random = random.SystemRandom()


def _db_get(key):
    out = _db.execute(
        'select value from keyvalue where key = ?', (key,)).fetchone()
    if out is None:
        return None
    return out[0]


def _db_set(key, value):
    _db.execute(
        'insert or replace into keyvalue (key, value) values (?, ?)',
        (key, value))
    _db.commit()


def depends(*nodes):
    '''
    Runs the wrapped function if any dependency has changed.

    Dependency nodes can be either other functions wrapped with depends or
    checks.
    '''
    def wrap_function(function):
        class _Rule(object):
            def __init__(self):
                self._unique = '{} {}'.format(
                    function.__name__,
                    md5(''.join(
                            node.unique() for node in nodes
                        ).encode('utf-8')).hexdigest())
                self._changed = any(node.changed(self) for node in nodes)
                if self._changed:
                    logger.info('Running {}'.format(function.__name__))
                    function()
                    self._invocation = json.dumps([
                        int(time.time() * 1000),
                        _random.random()])
                    _db_set(self._unique, self._invocation)
                    for node in nodes:
                        node.commit_changed(self)
                else:
                    self._invocation = _db_get(self._unique)

            def unique(self):
                return self._unique

            def changed(self, base):
                k = json.dumps([self._unique, base.unique()])
                return _db_get(k) != self._invocation

            def commit_changed(self, base):
                k = json.dumps([self._unique, base.unique()])
                _db_set(k, self._invocation)

        return _Rule()
    return wrap_function


def check(function):
    '''
    Converts a function that returns a key, value into a function that can be
    used as a dependency.

    The key should be a unique id for the object being checked.
    The value should be a value representing the state of the object.  If the
    value changes compared to a previous invocation, the dependant method will
    run.
    '''
    def inner(*pargs, **kwargs):
        k, v = function(*pargs, **kwargs)
        if not isinstance(k, (list, tuple)):
            k = (k,)
        k = json.dumps((function.__name__,) + k)
        v = str(v)
        logger.debug('Cached check: {}, {}'.format(repr(k), repr(v)))

        class _Check(object):
            def unique(self):
                return k

            def changed(self, base):
                k2 = json.dumps([k, base.unique()])
                v_old = _db_get(k2)
                if v == v_old:
                    return False
                return True

            def commit_changed(self, base):
                k2 = json.dumps([k, base.unique()])
                _db_set(k2, v)

        return _Check()
    return inner


@check
def file(path):
    '''Check for changes in a single file by timestamp.'''
    try:
        return path, int(os.path.getmtime(path) * 1000)
    except FileNotFoundError:
        return path, 0


def _update_hash(path, cs):
    with open(path, 'rb') as source:
        while True:
            data = source.read(4096)
            if not data:
                break
            cs.update(data)


@check
def file_hash(path):
    '''Check for changes in a single file by hash.'''
    cs = md5()
    try:
        _update_hash(path, cs)
        return path, cs.hexdigest()
    except FileNotFoundError:
        return path, 0


def _tree(path, depth, ignore, start, update, finish):
    ignore = [
        re.compile(pattern) if isinstance(pattern, str) else pattern
        for pattern in ignore
    ]
    if not path.endswith('/'):
        path = path + '/'
    state = start()
    for depth_, (root, dirs, files) in enumerate(os.walk(path)):
        if depth > 0 and depth_ > depth:
            break
        for file in files:
            full_file = os.path.join(root, file)
            if any(pattern.find(full_file) for pattern in ignore):
                continue
            state = update(state, full_file)
    return (path, depth), finish(state)


@check
def tree(path, depth=0, ignore=None):
    '''
    Check for changes in a file tree by timestamp.

    depth indicates how many levels to descend into the path. 0 is unlimited,
    1 is only the specified directory itself, 2 would include the first
    children, etc.

    ignore is a list of file and directory patterns to ignore.  Each pattern
    is a compiled regex applied against the file path from the tree root.
    '''
    return _tree(
        path,
        depth,
        ignore,
        lambda: 0,
        lambda state, path: state + os.path.getmtime(path),
        lambda state: state,
    )


@check
def tree_hash(path, depth=0, ignore=None):
    '''
    Check for changes in a file tree by hash.

    depth indicates how many levels to descend into the path. 0 is unlimited,
    1 is only the specified directory itself, 2 would include the first
    children, etc.

    ignore is a list of file and directory patterns to ignore.  Each pattern
    is a compiled regex applied against the file path from the tree root.
    '''
    return _tree(
        path,
        depth,
        ignore,
        lambda: md5(),
        lambda state, path: _update_hash(path, state),
        lambda state: state.hexdigest(),
    )


def raw_check(function):
    '''
    Converts a function that returns a key, value into a function that can be
    used as a dependency.

    The key should be a unique id for the object being checked.
    The value should be True if the dependant function should run.
    '''
    def inner(*pargs, **kwargs):
        k, v = function(*pargs, **kwargs)
        if not isinstance(k, (list, tuple)):
            k = (k,)
        k = json.dumps((function.__name__,) + k)
        logger.debug('Raw check: {}, {}'.format(repr(k), repr(v)))

        class _Check(object):
            def unique(self):
                return k

            def changed(self, base):
                return v

            def commit_changed(self, base):
                pass

        return _Check()
    return inner


@raw_check
def nofile(path):
    '''Check if a file does not exist.'''
    return path, not os.path.exists(path)

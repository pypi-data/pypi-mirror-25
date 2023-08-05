import json
import logging
import os
import re
import tempfile

import atexit
import traceback

import colored

import datetime

from dnutils import ifnone
from dnutils.debug import _caller
from dnutils.threads import sleep, RLock
from dnutils.tools import jsonify

import portalocker
FLock = portalocker.Lock


DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

FileHandler = logging.FileHandler
StreamHandler = logging.StreamHandler


_expose_basedir = '.exposure'
_exposures = None
_writelockname = '.%s.lock'


def tmpdir():
    '''
    Returns the path for temporary files.

    On Unix systems, eg. mostly ``/tmp``
    :return:
    '''
    with tempfile.NamedTemporaryFile(delete=True) as f:
        return os.path.dirname(f.name)


class ExposureEmptyError(Exception): pass


class ExposureLockedError(Exception): pass


def active_exposures(name='/*'):
    '''
    Generates the names of all exposures that are currently active (system-wide).

    :param name:    a pattern that the list of exposure names can be filtered (supports the wildcard character *)
    :return:
    '''
    tmp = tmpdir()
    rootdir = os.path.join(tmp, _expose_basedir)
    for root, dirs, files in os.walk(rootdir):
        for f in files:
            if re.match(r'\.\w+\.lock', f):  # skip file locks
                continue
            try:
                tmplock = FLock(os.path.join(root, _writelockname % f), timeout=0, fail_when_locked=True)
                tmplock.acquire()
            except portalocker.LockException:
                expname = '/'.join([root.replace(rootdir, ''), f])
                tokens = expname.split('/')
                patterns = name.split('/')
                ok = False
                for idx, pat in enumerate(patterns):
                    try:
                        repattern = '^%s$' % re.escape(pat).replace(r'\*', r'.*?')
                        ok = re.match(repattern, tokens[idx]) is not None
                    except IndexError:
                        ok = False
                    if not ok: break
                else:
                    if ok:
                        yield expname
            else:
                tmplock.release()


class ExposureManager:
    '''
    Manages all instances of exposures.
    '''

    def __init__(self, basedir=None):
        self.exposures = {}
        self.basedir = ifnone(basedir, tmpdir())

    def create(self, name, mode):
        '''
        Create a new exposure with name ``name`` and mode ``mode``.

        :param name:
        :param mode:
        :return:
        '''
        e = Exposure(name, mode, self.basedir)
        self.exposures[(name, mode)] = e
        atexit.register(_cleanup_exposures)
        return e

    def close(self):
        for name, exposure in self.exposures.items():
            exposure.close()


def _cleanup_exposures(*_):
    _exposures.close()


def exposures(basedir='.'):
    global _exposures
    _exposures = ExposureManager(basedir)


def expose(name, *data):
    '''
    Expose the data ``data`` under the exposure name ``name``.
    :param name:
    :param data:
    :return:
    '''
    global _exposures
    if _exposures is None:
        _exposures = ExposureManager()
    if (name, 'w') in _exposures.exposures:
        e = _exposures.exposures[(name, 'w')]
    else:
        e = _exposures.create(name, 'w')
    if data:
        if len(data) == 1:
            data = data[0]
        e.dump(data)
    return e


def inspect(name):
    '''
    Inspect the exposure with the name ``name``.
    :param name:
    :return:
    '''
    global _exposures
    if _exposures is None:
        _exposures = ExposureManager()
    if (name, 'r') in _exposures.exposures:
        e = _exposures.exposures[(name, 'r')]
    else:
        e = _exposures.create(name, 'r')
    return e.load()


class Exposure:
    '''
    This class implements a data structure for easy and lightweight exposure of
    parts of a program's state. An exposure is, in essence, a read/write
    wrapper around a regular file, which is being json data written to and read from.
    '''

    def __init__(self, name, mode='w', basedir=None):
        if basedir is None:
            basedir = tmpdir()
        basedir = os.path.join(basedir, _expose_basedir)
        if not os.path.exists(basedir):
            os.mkdir(basedir)
        dirs = list(os.path.split(name))
        if not dirs[0].startswith('/'):
            raise ValueError('exposure names must start with "/"')
        else:
            dirs[0] = dirs[0].replace('/', '')
        fname = dirs[-1]
        fullpath = basedir
        for d in dirs[:-1]:
            fullpath = os.path.join(fullpath, d)
            if not os.path.exists(fullpath):
                os.mkdir(fullpath)
        self.fullpath = os.path.abspath(fullpath)
        exposure_file = os.path.join(self.fullpath, fname)
        # acquire the lock if write access is required
        self.flock = None
        try:
            if mode == 'w':
                flockname = os.path.join(self.fullpath, _writelockname % fname)
                self.flock = FLock(flockname, timeout=0, fail_when_locked=True)
                self.flock.acquire()
        except portalocker.LockException as e:
            raise ExposureLockedError from e
        self.name = name
        self.mode = mode
        if mode == 'w':
            mode = 'w+'
        try:
            self.file = open(exposure_file, mode)
        except FileNotFoundError as e:
            raise ExposureEmptyError() from e
        self._lock = RLock()

    def dump(self, item):
        '''
        Write the item to the exposure.

        :param item:
        :return:
        '''
        with self._lock:
            if self.mode != 'w':
                raise TypeError('exposure is read-only.')
            jsondata = jsonify(item)
            self.file.truncate(0)
            self.file.seek(0)
            json.dump(jsondata, self.file, indent=4)
            self.file.write('\n')
            self.file.flush()

    def close(self):
        '''
        Close this exposure.
        :return:
        '''
        with self._lock:
            if not self.file.closed:
                if self.mode == 'w':
                    self.file.truncate(0)
                    self.file.flush()
                    self.file.close()
                    self.flock.release()

    def load(self, block=1):
        '''
        Load the content exposed by this exposure.

        If ``block`` is ``True``, this methods blocks until the content of this exposure
        has been updated by the writer
        :return:
        '''
        with self._lock:
            self.file.seek(0)
            if self.file.read(1) == '':
                raise ExposureEmptyError()
            self.file.seek(0)
            return json.load(self.file)


class _LoggerAdapter(object):
    def __init__(self, logger):
        self._logger = logger
        self._logger.findCaller = self._caller

    def _caller(self, _):
        return _caller(4)

    def critical(self, *args, **kwargs):
        self._logger.critical(' '.join(map(str, args)), extra=kwargs)

    def exception(self, *args, **kwargs):
        self._logger.exception(' '.join(map(str, args)), extra=kwargs)

    def error(self, *args, **kwargs):
        self._logger.error(' '.join(map(str, args)), extra=kwargs)

    def warning(self, *args, **kwargs):
        self._logger.warning(' '.join(map(str, args)), extra=kwargs)

    def info(self, *args, **kwargs):
        self._logger.info(' '.join(map(str, args)), extra=kwargs)

    def debug(self, *args, **kwargs):
        self._logger.debug(' '.join(map(str, args)), extra=kwargs)

    def __getattr__(self, attr):
        return getattr(self._logger, attr)

    @property
    def level(self):
        return self._logger.level

    @level.setter
    def level(self, l):
        self._logger.setLevel(l)

    @property
    def name(self):
        return self._logger.name

    def add_handler(self, h):
        self._logger.addHandler(h)

    def rm_handler(self, h):
        self._logger.removeHandler(h)

    @property
    def handlers(self):
        return self._logger.handlers

    def new(self, name, level=None):
        '''
        Spawn a new logger with the given name and return it.

        The new logger will be a child logger of this logger, i.e. it will inherit all of its handlers and,
        if not specified by the level parameter, also the log level.

        :param name:
        :param level:
        :return:
        '''
        if level is None:
            level = self.level
        logger = logging.getLogger(name)
        logger.parent = self._logger
        logger._initialized = True
        logger.setLevel(level)
        return _LoggerAdapter(logger)

    def __str__(self):
        return '<LoggerAdapter name="%s", level=%s>' % (self.name, logging._levelToName[self.level])

def getloggers():
    with logging._lock:
        for name in logging.Logger.manager.loggerDict:
            yield getlogger(name)

def loglevel(level, name=None):
    if name is None:
        name = ''
    getlogger(name).level = level


ansi_escape = re.compile(r'\x1b[^m]*m')


def cleanstr(s):
    return ansi_escape.sub('', s)


class ColoredStreamHandler(logging.StreamHandler):
    def emit(self, record):
        self.stream.write(self.format(record))


colored_console = ColoredStreamHandler()


class ColoredFormatter(logging.Formatter):
    fmap = {
        logging.DEBUG: colored.fg('cyan') + colored.attr('bold'),
        logging.INFO: colored.fg('white') + colored.attr('bold'),
        logging.WARNING: colored.fg('yellow') + colored.attr('bold'),
        logging.ERROR: colored.fg('red') + colored.attr('bold'),
        logging.CRITICAL: colored.bg('dark_red_2') + colored.fg('white') + colored.attr('underlined') + colored.attr(
            'bold')
    }
    msgmap = {
        logging.DEBUG: colored.fg('cyan'),
        logging.INFO: colored.fg('white'),
        logging.WARNING: colored.fg('yellow'),
        logging.ERROR: colored.fg('red'),
        logging.CRITICAL: colored.fg('dark_red_2')
    }

    def __init__(self, formatstr=None):
        self.formatstr = formatstr

    def format(self, record):
        levelstr = colored.attr('reset')
        levelstr += ColoredFormatter.fmap[record.levelno]
        maxlen = max(map(len, logging._levelToName.values()))
        header = '%s - %s - ' % (datetime.datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S'),
                                 colored.stylize(record.levelname.center(maxlen, ' '), levelstr))
        return header + colored.stylize(('\n' + ' ' * len(cleanstr(header))).join(record.msg.split('\n')) + '\n',
                                        ColoredFormatter.msgmap[record.levelno])


colored_console.setFormatter(ColoredFormatter())

try:
    import pymongo
except ImportError:
    pass
else:
    class MongoHandler(logging.Handler):
        '''
        Log handler for logging into a MongoDB database.
        '''
        def __init__(self, collection):
            '''
            Create the handler.

            :param collection:  An accessible collection in a pymongo database.
            '''
            logging.Handler.__init__(self)
            self.coll = collection
            self.setFormatter(MongoFormatter())

        def emit(self, record):
            self.coll.insert(self.format(record))


    class MongoFormatter(logging.Formatter):

        def format(self, record):
            return {'message': record.msg , 'timestamp': datetime.datetime.utcfromtimestamp(record.created),
                    'module': record.module, 'lineno': record.lineno, 'name': record.name, 'level': record.levelname}


class LoggerConfig(object):
    '''
    Data structure for storing a configuration of a particular
    logger, such as its name and the handlers to be used.
    '''
    def __init__(self, level, *handlers):
        self.handlers = handlers
        self.level = level


def newlogger(*handlers, level=INFO):
    '''
    Create a new logger configuration.

    Takes a list of handlers and optionally a level specification.

    Example:
    >>> dnlog.newlogger(logging.StreamHandler(), level=ERROR)

    :param handlers:
    :param kwargs:
    :return:
    '''
    return LoggerConfig(level, *handlers)


def loggers(loggers=None):
    '''
    Initial setup for the logging of the current process.

    The root logger is identified equivalently by None or 'default'. If no specification for the root logger
    is provided, a standard console.rst handler will be automatically appended.

    :param loggers: a dictionary mapping the names of loggers to :class:`dnlog.LoggerConfig` instances.
    :return:
    '''
    if loggers is None:
        loggers = {}
    if not {None, 'default'} & set(loggers.keys()):
        loggers['default'] = newlogger(console)
    for name, config in loggers.items():
        logger = getlogger(name)
        for h in logger.handlers:
            logger.removeHandler(h)
        logger.level = config.level
        for handler in config.handlers:
            logger.add_handler(handler)
            logger._logger._initialized = True


def getlogger(name=None, level=None):
    '''
    Get the logger with the associated name.

    If name is None, the root logger is returned. Optionally, a level can be specified that the logger is autmatically
    set to.

    :param name:    the name of the desired logger
    :param level:   the log level
    :return:
    '''
    if name == 'default':
        name = None
    logger = logging.getLogger(name)
    defaultlevel = logging.getLogger().level
    adapter = _LoggerAdapter(logger)
    if not hasattr(logger, '_initialized') or not logger._initialized:
        logger.parent = None
        roothandlers = list(logging.getLogger().handlers)
        # clear all loggers first
        for h in logger.handlers:
            logger.removeHandler(h)
        # take default handlers from the root logger
        for h in roothandlers:
            adapter.add_handler(h)
        adapter.level = ifnone(level, defaultlevel)
        logger._initialized = True
    if level is not None:
        adapter.level = level
    return adapter


console = colored_console
loggers()


if __name__ == '__main__':

    # for i in range(10):

    expose('/vars/bufsize', 'hello')
    expose('/internal/state', 1)
    for ex in active_exposures():
        expose('/vars/bufsize', 'bla')
        # sleep(10)
        print(ex, inspect(ex))
        # portalocker.lock(f2, portalocker.LOCK_EX, timeout=0)

        # try:
        #     print(inspect('/vars/bufsize'))
        # except ExposureEmptyError:
        #     sys.exit(0)
        # sleep(5)


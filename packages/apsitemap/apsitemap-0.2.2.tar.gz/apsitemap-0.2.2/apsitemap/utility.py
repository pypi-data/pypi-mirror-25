#!/usr/bin/env python3
# encoding: utf-8
import logging
import sys
import logging.handlers

try:
    import colorama
except ImportError:
    colorama = None

try:
    import curses  # type: ignore
except ImportError:
    curses = None


def _stderr_supports_color():
    try:
        if hasattr(sys.stderr, 'isatty') and sys.stderr.isatty():
            if curses:
                curses.setupterm()
                if curses.tigetnum("colors") > 0:
                    return True
            elif colorama:
                if sys.stderr is getattr(colorama.initialise, 'wrapped_stderr',
                                         object()):
                    return True
    except Exception:
        pass
    return False


class ColoredFormatter(logging.Formatter):

    DEFAULT_FORMAT = '%(color)s[%(levelname)-8.8s %(asctime)s %(module)s:%(lineno)d]%(end_color)s %(message)s'
    DEFAULT_DATE_FORMAT = '%Y/%m/%d %H:%M:%S'
    DEFAULT_COLORS = {
        logging.DEBUG: 34,     # Blue
        logging.INFO: 32,      # Green
        logging.WARNING: 33,   # Yellow
        logging.ERROR: 31,     # Red
        logging.CRITICAL: 35,  # burgundy
    }

    def __init__(self, fmt=DEFAULT_FORMAT, datefmt=DEFAULT_DATE_FORMAT, style='%', color=True, colors=DEFAULT_COLORS):
        logging.Formatter.__init__(self, datefmt=datefmt)
        self._fmt = fmt
        self.style = style
        self._colors = {}
        if color and _stderr_supports_color():
            for levelno, code in colors.items():
                self._colors[levelno] = '\033[2;%dm' % code
            self._normal = '\033[0m'
        else:
            self._normal = ''

    def format(self, record):

        record.message = record.getMessage()
        record.asctime = self.formatTime(record, self.datefmt)
        if record.levelno in self._colors:
            record.color = self._colors[record.levelno]
            record.end_color = self._normal
        else:
            record.color = record.end_color = ''
        return self._fmt % record.__dict__


def standardize_url(url: str, scheme="http://"):

    if url.startswith("http://") or url.startswith("https://"):
        return url
    return scheme + url


def _get_logger():
    """generate logger"""
    logger = logging.Logger("sitemap")
    handler = logging.StreamHandler(stream=sys.stdout)
    formatter = ColoredFormatter()
    handler.setFormatter(fmt=formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    return logger


sitemap_log = _get_logger()

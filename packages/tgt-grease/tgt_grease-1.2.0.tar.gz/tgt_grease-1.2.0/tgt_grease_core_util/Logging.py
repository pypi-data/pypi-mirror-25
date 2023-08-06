import os
import time
import logging
from collections import deque
from logging.config import fileConfig
import random
from .Notifier import Notifier
from .Configuration import Configuration


class Logger:

    _config = Configuration()

    def __init__(self):
        self.start_time = time.time()
        self._messages = deque(())
        self._notifier = Notifier()
        # Setup Log Configuration
        if type(self._config.get('GREASE_LOG_FILE')) == str and os.path.isfile(self._config.get('GREASE_LOG_FILE')):
            fileConfig(self._config.get('GREASE_LOG_FILE'))
            self._logger = logging.getLogger('GREASE-' + str(random.random()))
        else:
            logFilename = self._config.grease_dir + self._config.fs_Separator + "grease.log"
            self._logger = logging.getLogger('GREASE-' + str(random.random()))
            self._logger.setLevel(logging.DEBUG)
            self._handler = logging.FileHandler(logFilename)
            self._handler.setLevel(logging.DEBUG)
            self._formatter = logging.Formatter("{\"timestamp\": \"%(asctime)s.%(msecs)03d\", \"level\" : \"%(levelname)s\", \"message\" : \"%(message)s\"}", "%Y-%m-%d %H:%M:%S")
            self._handler.setFormatter(self._formatter)
            self._logger.addHandler(self._handler)

    def __del__(self):
        self._logger.removeHandler(self._handler)

    def get_logger(self):
        # type: () -> logging
        return self._logger

    def get_messages(self):
        # type: () -> deque
        return self._messages

    def get_messages_dump(self):
        # type: () -> deque
        messages = self._messages
        self._messages = deque(())
        return messages

    def debug(self, message, verbose=False):
        # type: (str, bool) -> bool
        if verbose:
            if not self._config.get('GREASE_VERBOSE_LOGGING'):
                return True
            else:
                message = "VERBOSE::" + str(message).encode('utf-8')
        message = str(message).encode('utf-8')
        self._messages.append(('DEBUG', time.time(), message))
        return self._logger.debug(message)

    def info(self, message):
        # type: (str) -> bool
        message = str(message).encode('utf-8')
        self._messages.append(('INFO', time.time(), message))
        return self._logger.info(message)

    def warning(self, message):
        # type: (str) -> bool
        message = str(message).encode('utf-8')
        self._messages.append(('WARNING', time.time(), message))
        return self._logger.warning(message)

    def error(self, message):
        # type: (str) -> bool
        message = str(message).encode('utf-8')
        self._messages.append(('ERROR', time.time(), message))
        return self._logger.error(message)

    def critical(self, message):
        # type: (str) -> bool
        message = str(message).encode('utf-8')
        self._messages.append(('CRITICAL', time.time(), message))
        self._notifier.send_hipchat_message(message)
        return self._logger.critical(message)

    def exception(self, message):
        # type: (str) -> bool
        message = str(message).encode('utf-8')
        self._messages.append(('EXCEPTION', time.time(), message))
        self._notifier.send_hipchat_message(message)
        return self._logger.exception(message)

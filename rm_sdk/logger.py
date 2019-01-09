import sys
import logging
"""This module is for logging purpose and will set necessary log level
"""
class _MaxLevelFilter(object):
    def __init__(self, highest_log_level):
        self._highest_log_level = highest_log_level
    def filter(self, log_record):
        return log_record.levelno <= self._highest_log_level

# A handler for low level logs that should be sent to STDOUT
info_handler = logging.StreamHandler(sys.stdout)
info_handler.setLevel(logging.INFO)
info_handler.addFilter(_MaxLevelFilter(logging.WARNING))
# A handler for high level logs that should be sent to STDERR
error_handler = logging.StreamHandler(sys.stderr)
error_handler.setLevel(logging.ERROR)
logger = logging.getLogger()

logger.setLevel(logging.DEBUG) 
logger.addHandler(info_handler)
logger.addHandler(error_handler)
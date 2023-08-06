import logging

logger = logging.getLogger('IOMED CLI')
logger.setLevel(logging.DEBUG)
console = logging.StreamHandler()
logger.addHandler(console)
logger = logging.getLogger()

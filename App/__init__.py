import logging

def init_logging():
  logger = logging.getLogger('pythonBackendLogger')
  logger.setLevel(logging.DEBUG)
  ch=logging.StreamHandler()
  ch.setLevel(logging.DEBUG)
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  ch.setFormatter(formatter)
  logger.addHandler(ch)
  logger.info('logger initialized.')
  return logger

def get_logger():
  return logging.getLogger('pythonBackendLogger')

logger = init_logging()
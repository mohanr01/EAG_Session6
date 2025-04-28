import logging

logging.basicConfig(filename='app.log',level=logging.INFO, format='%(asctime)s-%(name)s-%(levelname)s-%(message)s')
logger = logging.getLogger(__name__)

def loggingInfo(message:str):
    logger.info(message)

def loggingError(message:str, exception:Exception):
    logger.exception(str,exception)

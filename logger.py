import logging
from datetime import datetime

def initialize_logger(logger_file_name = ""):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    # create a file handler saving files at ./data/logs/date.log
    handler = logging.FileHandler('./data/logs/' + datetime.now().strftime("%Y%m%d") + '.log')
    handler.setLevel(logging.INFO)
    # append a string of text to the start of each log message
    custom_text = logger_file_name + " - "
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - ' + custom_text +'%(message)s')
    # create a logging format and adding the filename into the format
    handler.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(handler)
    return(logger)


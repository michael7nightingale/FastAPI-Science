import logging
# import os


def create_logger():
    logger = logging.Logger(name='app_loger', level='DEBUG')
    file_handler = logging.FileHandler(filename='log/app.log')
    formatter = logging.Formatter("%(asctime)s   |   %(levelname)s   |   %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


logger = create_logger()



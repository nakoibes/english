import logging


class Config:
    SWAP_SIZE = 50

    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_LEVEL = logging.INFO
    LOG_FILENAME = 'app.log'
    LOG_FILEMOD = 'w'

import logging
import logging.config


def _logger():
    # create logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # add formatter to ch
    ch.setFormatter(logging.basicConfig(format='%(asctime)s:%(levelname)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S'))

    # add ch to logger
    if not logger.hasHandlers():
        logger.addHandler(ch)

    return logger

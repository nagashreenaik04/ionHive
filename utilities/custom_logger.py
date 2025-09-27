import logging

from selenium.webdriver.common.bidi.cdp import logger


class LogGen:
    @staticmethod
    def loggen():
        logging.basicConfig(filename=".\\logs\\automation.logs",format='%(asctime)s:%(levelname)s:%(message)s',
                            datefmt="%Y-%m-%d %H:%M:%S",force=True)
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        return logger

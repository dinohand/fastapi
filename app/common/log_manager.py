from app.common.config_manager import Config_Manager

import logging, coloredlogs
import datetime


# LOG Level
# NOTSET=0
# DEBUG=10
# INFO=20
# WARN=30
# ERROR=40
# CRITICAL=50

class Log_Manager:
    """_summary_ : logger를 생성하여 리턴한다
    """
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Log_Manager, cls).__new__(cls)
            print(f'{datetime.datetime.now()}-({__name__}) is initialized')
        return cls.instance
    
    def __init__(self) -> None:
        pass
    
    def getLogger(self, name):
        cm = Config_Manager()
        log_level = cm.properties['DEFAULT']['LOG_LEVEL'] if 'LOG_LEVEL' in cm.properties['DEFAULT'] else '30'
        log_file = cm.properties['DEFAULT']['LOG_FILE'] if 'LOG_FILE' in cm.properties['DEFAULT'] else 'app.log'

        logger = logging.getLogger(name)   
        logger.setLevel(int(log_level))

        ## log file
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setLevel(int(log_level))

        # log console
        ch = logging.StreamHandler()
        ch.setLevel(int(log_level))

        # log format
        formatter = logging.Formatter( '%(asctime)s : [%(name)s] [%(levelname)s] - %(message)s')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        logger.addHandler(ch)
        logger.addHandler(fh)

        coloredlogs.install()

        return logger
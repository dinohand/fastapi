from configparser import ConfigParser
from app.common.entities import ORACLE_DB
import os, datetime

class Config_Manager:
    ## 
    properties = None
    ora_info =  None
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config_Manager, cls).__new__(cls)
            
            run_mode = os.getenv("RUN_MODE")

            if not( run_mode == 'PRD' or run_mode =='DEV') : run_mode = 'TEST'
            cfg = ConfigParser()
            
            config_file = os.getcwd() + "/app/config/"+ run_mode.lower() + "_config.ini"
            cfg.read( config_file, encoding='UTF-8')
            
            oracle_db = ORACLE_DB()
            oracle_db.NAME = cfg['DATABASE']['NAME']
            oracle_db.HOST = cfg['DATABASE']['HOST']
            oracle_db.PORT = cfg['DATABASE']['PORT']
            oracle_db.USER_ID = cfg['DATABASE']['USER_ID']
            oracle_db.USER_PW = cfg['DATABASE']['USER_PW']
            oracle_db.DB_NAME = cfg['DATABASE']['DB_NAME']
            
            Config_Manager.ora_info = oracle_db
            Config_Manager.properties = cfg 

            print(f'{datetime.datetime.now()}-({__name__}) is initialized')
        return cls.instance     
        
    def __init__(self) -> None:
        pass
    
    def getProperty(self, sec:str, key:str) -> str | None:
        """Section과 Key해당되는 value를 리턴한다

        Args:
            sec (str): section
            key (str): key
        Returns:
            any : key에 지정된 값
        """
        try:
            return self.properties[sec][key]
        except:
            return None
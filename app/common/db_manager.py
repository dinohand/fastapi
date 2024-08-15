import oracledb

from app.common.config_manager import Config_Manager
from app.common.log_manager import Log_Manager
from app.common.entities import ORACLE_DB
from app.common.const import *

from impala.dbapi import connect # pip install impyla
import sys

import pandas as pd
import numpy as np

# import inspect
# import typing

logger = Log_Manager().getLogger('DATA')

class DB_Manager():
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DB_Manager, cls).__new__(cls)
        return cls.instance     

    def __init__(self) -> None:
        logger = Log_Manager().getLogger(type(self).__name__)

    def gegSQLite(self, conn_str):
        conn = sqlite3.connect(conn_str)
        return conn

    def getOracle(self, ora_info: ORACLE_DB ):
    # def getOracle(self, user_id:str, pswd:str, host:str, db_port:string, port:str , db_name:str ) -> Connection :
    #     con = oracledb.connect(user="scott", password="tiger", dsn="192.168.1.171:1521/ORA19")
        parent_frame = sys._getframe(1).f_code.co_name
        # current_frame = inspect.getframeinfo(inspect.currentframe()).function
        try:
            conn = oracledb.connect( user=ora_info.USER_ID , password=ora_info.USER_PW, dsn= ora_info.HOST + ':' + ora_info.PORT + '/' + ora_info.DB_NAME )
            return conn
        except Exception as e:
            logger.error(str(e))
            
            data = {"Exception" : str(e), "caller": parent_frame}
            return MSG_FAIL | { "result" : data }
        finally:
            pass
    
    def make_dic_factory(self, cursor):
        column_names = [d[0] for d in cursor.description]

        def create_row(*args):
            return dict(zip(column_names, args))
        return create_row

    ## '%' string 대입을 위한 tuple을 만든다
    def make_tuple(self, param : tuple | str ):
        if param is None: return ('',)
        elif type(param) == list: return tuple(param)
        elif type(param) == tuple:
            li = []
            for k in param:
                if k is None or k =='None' : li.append('')  
                else: li.append(k)
            return tuple(li)
        else:
            return (param,)
    
    # sql select문을 실행한다
    def select(self, qry : str, param : tuple | str):
        parent_frame = sys._getframe(1).f_code.co_name
        # current_frame = inspect.getframeinfo(inspect.currentframe()).function

        sql = qry%self.make_tuple(param)
        conn = self.getOracle(ora_info=Config_Manager().ora_info)
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            
            cursor.rowfactory = self.make_dic_factory(cursor)
            res = cursor.fetchall()
            
            # column_names = [desc[0] for desc in cursor.description]
            # # res = pd.DataFrame( cursor.fetchall() , columns=column_names )
            # res = pd.DataFrame( cursor.fetchall()  )
            
            data = {"data": res , "sql": sql}
            return MSG_SUCCESS | { "result" : data }
         
        except Exception as e:
            logger.error(str(e))
            data = {"Exception" : str(e), "sql": sql}
            
            return MSG_FAIL | { "result" : data }
        finally:
            cursor.close()
            conn.close()

    # insert/update/delete등의 transaction 관리가 필요한 sql 문을 실행한다
    def execute(self, qry : str, param : tuple) -> dict:
        """쿼리문을 실행한다
            select문은 select() nethod를 실행한다
        Args:
            qry (str): 쿼리문
            param (tuple): 쿼리문에 사용되는 파라미터
        Returns:
            dict: 실행 결과
        """
        parent_frame = sys._getframe(1).f_code.co_name
        # current_frame = inspect.getframeinfo(inspect.currentframe()).function
        
        sql = qry%self.make_tuple(param)

        conn = self.getOracle(ora_info=Config_Manager().ora_info)
        conn.autocommit(False)
        conn.begin()
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            
            data = {"data":res , "caller": parent_frame,  "rowcount": cursor.rowcount, "sql": sql }
            return MSG_SUCCESS | { "result": data }
        except Exception as e:
            conn.rollback()
            
            logger.error(str(e))
            data = {"Exception" : str(e), "caller": parent_frame, "sql": sql}
            return MSG_FAIL | { "result" : data }
        finally:
            cursor.close()
            comm.close()
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
        # logger = Log_Manager().getLogger(type(self).__name__)
        pass

    def _geg_SQLite(self, conn_str : str):
        """SQLite connection을 리턴한다

        Args:
            conn_str (str): connection string

        Returns:
            connection : SQLite connection
        """        
        conn = sqlite3.connect(conn_str)
        return conn

    def _get_Oracle(self, ora_info: ORACLE_DB ) -> oracledb.Connection:
        """Oralce Connection객체를 리턴한다
        Args:
            ora_info (ORACLE_DB): 오라클 conection 정보
        Returns:
            connection : oracledb.Connection
        """
        parent_frame = sys._getframe(1).f_code.co_name
        # current_frame = inspect.getframeinfo(inspect.currentframe()).function
        try:
            conn = oracledb.connect( user=ora_info.USER_ID , password=ora_info.USER_PW, dsn= ora_info.HOST + ':' + ora_info.PORT + '/' + ora_info.DB_NAME )
            return conn
        except Exception as e:
            msg = CR + str(e) + CR + f"caller:{parent_frame}"
            logger.error(msg)
            
            data = {"Exception" : str(e), "caller": parent_frame}
            return MSG_FAIL | { "result" : data }
        finally:
            pass

    def get_conn(self, db_type : str = 'oracle', conn_str : str = '') : #  class 상속시 get_conn()을 override한다
        """db_type 에 따른 db connection을 리턴한다

        Args:
            db_type (str, optional):  Database type. Defaults to 'oracle'.
            conn_str (str, optional): Connection strng. Defaults to ''.

        Raises:
            Exception: does not support Database Exception

        Returns:
            connection : connection
        """ 
        if db_type.lower() == 'oracle':
            return self._get_Oracle(ora_info=Config_Manager().ora_info)
        elif db_type.lower() == 'sqlite':
            return self._geg_SQLite(conn_str)
        else:
            raise Exception("does not support")

    ## '%' string 대입을 위한 tuple을 만든다
    def _make_tuple(self, param : tuple | list | str) -> tuple:
        """param을 tuple 형태로 리턴한다
        
            ex) make_tuple(None) returns ('',)
                make_tuple(()) returns ()
        Args:
            param (tuple | list | str): tuple 형태로 리턴할 입력 값

        Returns:
            tuple: tuple value
        """
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
    def select(self, query : str, param : tuple = (), result_type : str =  'records' ):
        """쿼리문을 실행한다
            select문을 실행한다
        Args:
            qry (str): 쿼리문
            param (tuple): 쿼리문에 사용되는 파라미터
        Returns:
            dict: 실행 결과
        """
        parent_frame = sys._getframe(1).f_code.co_name # 호출한 객체(function, module,,,)를 알아낸다
        # current_frame = inspect.getframeinfo(inspect.currentframe()).function

        sql = query%self._make_tuple(param)
        
        conn = self.get_conn(db_type='oracle')
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            res = cursor.fetchall()
            
            column_names = [desc[0] for desc in cursor.description]
            
            df = pd.DataFrame(res, columns=column_names)
            df = df.fillna('')      ## None / null 처리, 하지 않으면 Out of range float values are not JSON compliant 에러 발생함
            return MSG_SUCCESS | { "result" : df.to_dict(orient=result_type) }
        except Exception as e:
            msg = CR + str(e) + CR + f"caller:{parent_frame}" + CR + f"sql:{sql}"
            logger.error(msg)
            
            return MSG_FAIL | {"Exception" : str(e), "caller": parent_frame , "sql": sql}
        finally:
            cursor.close()
            conn.close()

    # insert/update/delete등의 transaction 관리가 필요한 sql 문을 실행한다
    def execute(self, query : str, param : tuple = ('',)) -> dict:
        """쿼리문을 실행한다
            select문은 select() method를 실행한다
        Args:
            qry (str): 쿼리문
            param (tuple): 쿼리문에 사용되는 파라미터
        Returns:
            dict: 실행 결과
        """
        parent_frame = sys._getframe(1).f_code.co_name
        # current_frame = inspect.getframeinfo(inspect.currentframe()).function
        
        sql = query%self._make_tuple(param)

        conn = self.get_conn(db_type='oracle')
        conn.autocommit(False)  # transaction
        conn.begin()
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            
            return MSG_SUCCESS | {  "rowcount": cursor.rowcount, "caller": parent_frame} 
        except Exception as e:
            conn.rollback()
            msg = CR + str(e) + CR + f"caller:{parent_frame}" + CR + f"sql:{sql}"
            logger.error(msg)

            return MSG_FAIL | {"Exception" : str(e), "caller": parent_frame ,  "sql": sql}
        finally:
            cursor.close()
            comm.close()


    # result 에 colums를 dict로 zip하여 리턴한다
    # def make_dic_factory(self, cursor):
    #     column_names = [d[0] for d in cursor.description]

    #     def create_row(*args):
    #         return dict(zip(column_names, args))
    #     return create_row
import oracledb

from app.common.config_manager import Config_Manager
from app.common.log_manager import Log_Manager
from app.common.entities import ORACLE_DB
from app.common.const import *


class DB_Manager:
    logger = None
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DB_Manager, cls).__new__(cls)
        return cls.instance     

    def __init__(self) -> None:
        logger = Log_Manager().getLogger(type(self).__name__)

    # def gegSQLite(self, conn_str):
    #     conn = sqlite3.connect(conn_str)
    #     return conn
    
    def getOracle(self, ora_info: ORACLE_DB ):
    # def getOracle(self, user_id:str, pswd:str, host:str, db_port:string, port:str , db_name:str ) -> Connection :
    #     con = oracledb.connect(user="scott", password="tiger", dsn="192.168.1.171:1521/ORA19")
        try:
            conn = oracledb.connect( user=ora_info.USER_ID , 
                                            password=ora_info.USER_PW, 
                                            dsn= ora_info.HOST + ':' + ora_info.PORT + '/' + ora_info.DB_NAME )

            return conn
        except Exception as e:
            print(e)
            return {"message":e,"status":400}
        finally:
            pass
    
    def make_dic_factory(self, cursor):
        column_names = [d[0] for d in cursor.description]

        def create_row(*args):
            return dict(zip(column_names, args))
        return create_row
        
    def select(self, qry : str, param : tuple) :
        """Select query문을 실행행한다

        Args:
            qry (str): 쿼리문
            param (tuple): 쿼리문에 사용되는 파라미터

        Returns:
            dict : 실행 결과 
        """
        conn = self.getOracle(ora_info=Config_Manager().ora_info)
        
        try:
            cursor = conn.cursor()
            cursor.execute(qry, param)
            cursor.rowfactory = self.make_dic_factory(curs)
             
            res = cursor.fetchall()
            
            data = {"data":res , "sql": qry}
                    
            return MSG_SUCCESS | { "result" : data } 
        except Exception as e:
            logger.error(str(e))
            data = {"Exception" : str(e), "sql": qry}
            return MSG_FAIL | { "result" : data }
        finally:
            cursor.close()
            conn.close()


    def execute(self, qry : str, param : tuple) -> dict:
        """쿼리문을 실행한다
            select문은 select() nethod를 실행한다
        Args:
            qry (str): 쿼리문
            param (tuple): 쿼리문에 사용되는 파라미터
        Returns:
            dict: 실행 결과
        """
        conn = self.getOracle(ora_info=Config_Manager().ora_info)

        conn.autocommit(False)
        conn.begin()
        try:
            cursor = conn.cursor()
            cursor.execute(qry, param)

            conn.commit()
            
            data = {"data":res , "rowcount": cursor.rowcount, "sql": qry }
            return MSG_SUCCESS | { "result": data }
        except Exception as e:
            conn.rollback()
            
            logger.error(str(e))
            data = {"Exception" : str(e), "sql": qry}
            return MSG_FAIL | { "result" : data }
        finally:
            cursor.close()
            comm.close()
    
# class Ora_Conn(DB_Manager):
#     ora_conn = None
#     # def __new__(cls):
#     #     if not hasattr(cls, 'instance'):
#     #         cls.instance = super(Ora_Conn, cls).__new__(cls)
#     #     return cls.instance     
    
#     def __init__(self):
#         # super.__init__(self)
#         conn = super.getOracle(Config_Manager().ora_info)
#         Ora_Conn.ora_conn = conn 
        
    
#     def getConn():
#         super.getOracle(Config_Manager().ora_info)
        
#         return super.getOracle()
#     def select(self, sql: str):
#         pass        
    
#     def insert(self, sql:str):
#         pass
    
#     def execute(self, sql:str):
#         msg = None
#         sts = None
#         try:
#             curs = Ora_Conn().ora_conn.cursor()

#             rs = curs.execute(sql)
#             msg = '성공'
#             sts = 200
#         except Exception as e:
#             logger.error(e)
#             msg = '실패'
#             sts = 300
#         finally:
#             curs.close()     
#         return { "message":msg, "status":sts}

# class SQLite(DB_Manager):
#     def __init__(self):
#         super.__init__(self)
    
#     def getConn():
#         pass
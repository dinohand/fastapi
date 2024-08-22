from fastapi import FastAPI
from fastapi import Request, Response, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.common.log_manager import Log_Manager
from app.common.db_manager import DB_Manager
from app.common.config_manager import Config_Manager

from app.biz.queries import *
from app.common.const import *
from app.biz.models import *

logger = Log_Manager().getLogger("BIZ")

# 라우트에 따른 처리 프로세스
class Route_Service:
    def __init__(self) -> None:
        # self_name = Log_Manager().getLogger( type(self).__name__ )
        self.templates = Jinja2Templates(directory="static")   ### templates.TemplateResponse를 사용하려면 Route_Service에서 선언되어야 있어야 한다

    ## root page route
    async def root(self) -> str:
        status_code = 200
        message =  "This is root page !"
        return {"message": message, "code": status_code}

    async def heathCheck(self) -> str:
        # self.logger.info("health check ---------------")
        return {"message":"ok", "code":200}
    
    def hello(self):
        # self.logger.info("hello----------------")
        return "You need REST Api call"
# -----------------------------------------------------------------------
    def select_all_test(self):
        sql = QUERY_STR['test'].get('select_all')
        res  = DB_Manager().select(sql, ())
        
        # if res["status"] == OK: 
        #     logger.info(res["result"])
        # else:
        #     logger.info(res)            
        
        return res
    
    def select_error(self):
        sql = QUERY_STR['test'].get('select_error')
        res  = DB_Manager().select(sql, ())
        
        # if res["status"] == OK: 
        #     logger.info(res["result"])
        # else:
        #     logger.info(res)            
        
        return res
    
    
    def select_multi(self):
        sql = QUERY_STR['test'].get('select_all')
        res  = DB_Manager().select(sql, ())
        
        res2 = DB_Manager().select("select count(*)  as CNT from dual", ())
        
        if res["status"] != OK:  return res
        if res2["status"] != OK:  return res2
        
        result = []
        result.append( {"mst": res["result"]} )
        result.append( {"branch" : res2["result"]} )
            
        print('==========================================================')
        print(f"res_mst[1].get('branch')[0].get('CNT') = {result[1].get('branch')[0].get('CNT')}")
        print(f"res_mst[1][]'branch'][0]['CNT'] = {result[1]['branch'][0]['CNT']}")
        
        return MSG_SUCCESS | { "result" : result}
    
    def select_test(self, dict_m : DICT_M ):
        sql = QUERY_STR['test'].get('select')
        
        # param = (dict_m.VALUE )
        return DB_Manager().select(sql, ( dict_m.VALUE, )  )
        # return DB_Manager().select(sql, ( None )  )

# -----------------------------------------------------------------------
    async def insert_test(self):
        sql = QUERIES_STR['test'].get('insert')
        return DB_Manager().select(sql, ()) 

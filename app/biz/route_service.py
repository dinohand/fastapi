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



# 라우트에 따른 처리 프로세스
class Route_Service:
    logger = None
    def __init__(self) -> None:
        self.logger = Log_Manager().getLogger( type(self).__name__ )
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
    async def select_all_test(self):
        sql = QUERY_STR['test'].get('select_all')
        return DB_Manager().select(sql, ())
    
    def select_test(self, dict_m : DICT_M ):
        sql = QUERY_STR['test'].get('select')
        return DB_Manager().select(sql, (dict_m.VALUE))
    
    

# -----------------------------------------------------------------------
    async def insert_test(self):
        sql = QUERIES_STR['test'].get('insert')
        return DB_Manager().select(sql, ()) 

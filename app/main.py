from fastapi import FastAPI
from fastapi import Response, Request, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from typing import Annotated

from app.common.config_manager import Config_Manager
from app.common.log_manager import Log_Manager
from app.biz.route_service import Route_Service
from app.biz.queries import *
from app.common.const import *
from app.biz.models import *
from PIL import Image

# from app.common.init import *
import os


#------------------------------------------------------
# 초기 설정
# 1. 필요한 디렉토리를 생성한다
dirs = ['NAS/REF' ,  'NAS/CODE']
cwd = os.getcwd()

# 필수 디렉토리 생성
for dir in dirs :
    new_dir = cwd + "/" + dir
    if os.path.isdir(new_dir) ==False: 
        os.makedirs(new_dir)
        logger.info(f'{new_dir} folder is created')

# 2. logger 설정
cm = Config_Manager() ## config manager
rs = Route_Service()


logger = Log_Manager().getLogger("MAIN")
logger.info( f'Main Module({__file__}) is activated' )

_root_path ='/api/v1'
#----------------------------------------------------------
app = FastAPI(
            # swagger_ui_parameters=swagger_ui_default_parameters,
            swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
            title='title',
            summary='summary',
            description='Boilerplate',
            version='0.1',
            root_path=_root_path,
            docs_url='/docs',
            # redoc_url='/api/v1/redocs',
            terms_of_service="", ## "http://example.com/terms/",
            contact={
                "name": "JK.Youk",
                "url":  "https://github.com/dinohand",
                "email": "excelon@live.co.kr",
            },            
            license_info={
                "name": "Apache 2.0",
                "identifier": "MIT",
                #  "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
            },
        )

#-- CORS Env
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# set static folder
app.mount("/home", StaticFiles(directory="home"), name="home")
app.mount("/NAS", StaticFiles(directory="NAS"), name="NAS")

#---------------------------------------------------
@app.get('/')
async def read_item():
    redirect_url = f'{_root_path}/home/index.html'
    return RedirectResponse(redirect_url, status_code=303)
    # return await rs.root()

async def check_health():
    return await rs.heathCheck()

@app.post('/fileupload')
async def upload():
    f = request.files['file']
    f.save(f.filename)
    return '성공 여부 try except로 처리 계획' 

#---------------------------------------------------
@app.post("/select_all_test", tags=['Test'])
def select_all_test():
    return rs.select_all_test()

@app.post("/select_error", tags=['Test'])
def select_error():
    return rs.select_error()

@app.post("/select_multi", tags=['Test'])
def select_multi():
    return rs.select_multi()


@app.post("/select_test", tags=['Test'])
def select_test(
    *,
     dict_m: Annotated[
        DICT_M,
        Body(
            openapi_examples={
                "normal":{
                    "value":{
                            "VALUE": "Foo"
                    }
                }
            },
        ),
     ]
    ):
    
    return rs.select_test(dict_m)



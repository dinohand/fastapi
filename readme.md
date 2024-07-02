## 가상환경 구성
    \>py  -3.12  -m venv .venv

## 가상환경 활성화
    \>.venv\Scripts\activate

    ( 비활성화는 : \>.venv\Scripts\deactivate )

## 필요 라이브러리 설치
- 가상환경에서 라이브러리를 설치해야 가상환경에 반영됨
- 
    1) 개별적으로 하나씩 라이브러리 설치
        \>pip install fastapi

    2) 일관적으로 라이브러리 목록을 참조해서 설치
        \>pip install -r requirements.txt


## 실행방법
    - ASGI (Asynchronous Server Gateway Interface : 비동기 )-  
    - WSGI (Web Server Gateway Interface : 동기 전용)
    . uvicorn, hypercorn,
    . Gunicorn

    ASGI, WSGI -> CGI 와 같은 것

   c:\Dev\FastAPI>fastapi run --host 127.0.0.1 --port 5000

# vscode lauche.json 설정 방법
```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Prduct",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "app.main:app",
                "--host",
                "0.0.0.0",
                "--port",
                "5000",
                "--workers",
                "4"                
            ],
            "console": "integratedTerminal",
            "env": {
                "RUN_MODE":"PRD",
            }
        },
        {
            "name": "Develop",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "cwd": "${workspaceFolder}",
            "args": [
                "app.main:app",
                "--host",
                "0.0.0.0",
                "--reload",
                "--port",
                "5000"
            ],

            "console": "integratedTerminal",
            "env": {
                "RUN_MODE":"DEV",
            }
        },
        {
            "name": "Test File",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "env": {
                "RUN_MODE":"TEST",
            }
        },
    ]
}

```


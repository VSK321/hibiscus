from hibiscus.core.mvc import MVC
import uvicorn
import os

main_app = MVC()


def build():
    main_app.build()


async def app(scope, receive, send):
    await main_app.request_manager_async(send, receive, scope)

def runserver(app_path: str):
    os.chdir(app_path)
    port = 8000
    build()
    try:
        uvicorn.run(app, host="localhost", port=port)
    except KeyboardInterrupt:
        pass

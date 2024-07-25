import rose_mvc_framework

main_app = rose_mvc_framework.MVC()
def build():
    main_app.Build()

async def app(scope, receive, send):
    await main_app.HTTPRequestManagerAsync(send, receive, scope)
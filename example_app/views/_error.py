from hibiscus import view
from hibiscus import app


@app.set_route("/_error")
class Page(view.View):
    def __init__(self):
        pass

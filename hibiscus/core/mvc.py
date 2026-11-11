from builtins import KeyError
from types import ModuleType
import importlib
import mimetypes
import os
import glob
import sys
import pickle

from hibiscus.core.apploc import (
    app,
    backgroundtasks,
)
import hibiscus.core.compiler as compiler
import hibiscus.core.httpheaders as httpheaders


class MVC:
    def __init__(self):
        # super().__init__(host, port, backlog, threads)
        self.Critical_View: dict[str, ModuleType] = {}

    async def view_handler_async(self) -> tuple[list[tuple[str, str]], bytes]:
        """
        !TODO: Update to include paths using a new list called mvc_views OR update controllers to return mvc_views (add compiler for it)
        """
        headers = {
            "Server": "Hibiscus",
            "X-Frame-Options": "SameOrigin",
            "Cache-Control": "no-cache",
            "Content-Type": "text/html",
            "connection": "close",
        }
        headers = httpheaders.uvicorn_header_constructor(headers)
        response = await self.Critical_View["MainLayout"].Page().main()
        response = response.encode()
        return (headers, response)

    async def controller_handler_async(
        self,
        send,
        receive,
        scope,
        softpath: str,
        recognised_pattern: str,
        subs: dict[str, object],
    ) -> None:
        await app.funcs[recognised_pattern]["module"](
            **{
                "send": send,
                "receive": receive,
                "scope": scope,
                "Critical_View": self.Critical_View,
            }
        ).main()

    def public_handler(self, softpath: str) -> tuple[list[tuple[str, str]], bytes]:
        headers = {
            "Server": "Hibiscus",
            "X-Frame-Options": "SameOrigin",
            "Cache-Control": "no-cache",
            "Content-Type": mimetypes.guess_type(softpath)[0],
            "connection": "close",
        }
        cwd = os.getcwd()
        headers = httpheaders.uvicorn_header_constructor(headers)
        os.chdir(app.funcs[softpath]["hardpath"])
        f = open(app.funcs[softpath]["file"], "rb")
        response = f.read()
        f.close()
        os.chdir(cwd)
        return (headers, response)

    async def request_manager_async(self, send, receive, scope) -> None:
        if "path" in scope:
            softpath = scope["path"]  ###Check if softpath exists
        else:
            return None
        try:
            # Match softpath pattern
            found_pattern = None
            subs = {}
            for path_to_re in app.paths_to_re:
                if bool(path_to_re[0].fullmatch(softpath)):
                    found_pattern = path_to_re[1]
                    subs = {
                        tup[0][0]: getattr(sys.modules["builtins"], tup[0][1])(tup[1])
                        for tup in zip(path_to_re[2], softpath.split("/")[1:])
                        if tup[0] is not None
                    }
                    break
            if found_pattern is None:
                softpath_Type = app.funcs[softpath]["type"]
            else:
                softpath_Type = app.funcs[found_pattern]["type"]
            if softpath_Type == "view":
                (headers, response) = await self.view_handler_async()
                await send(
                    {"type": "http.response.start", "status": 200, "headers": headers}
                )
                await send({"type": "http.response.body", "body": response})
            elif softpath_Type == "controller":
                if found_pattern is None:
                    raise KeyError()
                await self.controller_handler_async(
                    send, receive, scope, softpath, found_pattern, subs
                )
            elif softpath_Type == "public":
                if found_pattern is not None:
                    raise KeyError
                (headers, response) = self.public_handler(softpath)
                await send(
                    {"type": "http.response.start", "status": 200, "headers": headers}
                )
                await send({"type": "http.response.body", "body": response})
        except KeyError as e:
            print("Page not found: " + str(e))
            (headers, response) = await self.view_handler_async()
            await send(
                {"type": "http.response.start", "status": 404, "headers": headers}
            )
            await send({"type": "http.response.body", "body": response})

    def build(self) -> None:
        print("Building...")
        cwd = os.getcwd()

        divider = "/"

        # Discover all files within cwd and check for .hibiscus and .py
        views = glob.glob("./**/*.hibiscus", recursive=True)
        controllers = glob.glob("./*/**/*.py", recursive=True)
        controllers = [
            controller
            for controller in controllers
            if controller[:-2] + "hibiscus" not in views
        ]
        os.chdir(cwd + "/root")
        public = glob.glob("./**/*.*", recursive=True)
        os.chdir(cwd)

        for f in os.listdir(os.getcwd() + "/shared"):
            if f.endswith(".hibiscus"):
                compiler.convert("./shared", f)

        for obj in public:
            path = obj.split(divider)
            name = path[-1]
            app.funcs["/" + "/".join(path[1:])] = {
                "type": "public",
                "file": (name),
                "hardpath": (cwd + "/root" + "/".join(path[1:-1])),
            }

        # Import and check for implementations of View or Controller
        for view in views:
            if view.startswith(f".{divider}shared"):
                continue
            with open(view, "r") as f:
                if f.read().startswith("#ignore\n"):
                    continue
            path = view.split(divider)
            compiler.convert(divider.join(path[0:-1]), path[-1])

        for f in os.listdir(os.getcwd() + "/shared"):
            if f.endswith(".hibiscus"):
                self.Critical_View[f[0:-9]] = importlib.import_module(
                    "shared." + f[0:-9]
                )
                m = "shared." + f[0:-9] + "c"
                importlib.import_module(m)
                os.remove("./shared/" + f[0:-9] + "c.py")

        for view in views:
            if view.startswith(f".{divider}shared"):
                continue
            with open(view, "r") as f:
                if f.read().startswith("#ignore\n"):
                    continue
            path = view.split(divider)
            value = ".".join(view.split(divider)[1:])[:-9]
            full_val = divider.join(path[0:-1]) + divider + path[-1][:-9] + "c.py"
            m = full_val[2:-3].replace(divider, ".")
            importlib.import_module(m)
            importlib.import_module(value)
            os.remove(full_val)

        for controller in controllers:
            with open(controller, "r") as f:
                if f.read().startswith("#ignore\n"):
                    continue
            value = ".".join(controller.split(divider)[1:])[:-3]
            importlib.import_module(value)

        # import hibiscusWS

        import hibiscus.controllers.hibiscusWS

        for task in backgroundtasks.funcs:
            task.main()  # type: ignore

        os.chdir(cwd)
        print("Build successful.")

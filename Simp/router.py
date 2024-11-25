from typing import Callable


class Router:
    def __init__(self):
        self.routes = {}

    def __call__(self):
        return self.routes

    def route(self, path: str,method: str, handler) -> Callable:
        # переменная для маршрутизации (По пути который передаём либо от названия хендлера)
        path_name = path or f"/{handler.__name__}"

        if path_name not in self.routes:
            self.routes[path_name] = {}

        self.routes[path_name][method] = handler
        return handler

    # декораторы маршрутизации по методам
    def get(self,path = None) -> Callable:
        def wrapper(handler):
            return self.route(path,"GET",handler)

        return wrapper

    def post(self,path = None) -> Callable:
        def wrapper(handler):
            return self.route(path,"POST",handler)

        return wrapper

    def put(self,path = None) -> Callable:
        def wrapper(handler):
            return self.route(path, "PUT", handler)

        return wrapper

    def patch(self,path = None) -> Callable:
        def wrapper(handler):
            return self.route(path, "PATCH", handler)

        return wrapper

    def delete(self,path = None) -> Callable:
        def wrapper(handler):
            return self.route(path, "DELETE", handler)

        return wrapper
from typing import Callable


class Router:
    def __init__(self, prefix: str = None):
        self.before_middleware = {}
        self.after_middleware = {}
        self.routes = {}
        self.prefix = prefix
        self.ws_routes = {}
        self.ws_before={}
        self.ws_after={}

    def __call__(self):
        return {
            'ws_routes':self.ws_routes,
            'ws_before':self.ws_before,
            'ws_after':self.ws_after,
            'routes':self.routes,
            'before_middleware':self.before_middleware,
            'after_middleware':self.after_middleware,
                }

    def route(self, path: str, method: str, handler , before_middleware = None, after_middleware = None) -> Callable:
        # переменная для маршрутизации (По пути который передаём либо от названия хендлера)
        # Задана для обработки префикса из роутера.
        if self.prefix is None:
            path_name = path or f"/{handler.__name__}"
        else:
            path_name = f"{self.prefix}{path}"

        if path_name not in self.routes:
            self.routes[path_name] = {}

        self.routes[path_name][method] = handler

        if before_middleware is not None or after_middleware is not None:
            self.before_middleware[path_name] = {}
            self.before_middleware[path_name][method] = before_middleware

        return handler

    # декораторы маршрутизации по методам
    def get(self,path = None, before = None ,after = None) -> Callable:
        def wrapper(handler):
            return self.route(path,"GET",handler, before_middleware=before, after_middleware=after)

        return wrapper

    def post(self,path = None, before = None ,after = None) -> Callable:
        def wrapper(handler):
            return self.route(path,"POST",handler, before_middleware=before, after_middleware=after)

        return wrapper

    def put(self,path = None, before = None ,after = None) -> Callable:
        def wrapper(handler):
            return self.route(path, "PUT", handler, before_middleware=before, after_middleware=after)

        return wrapper

    def patch(self,path = None, before = None ,after = None) -> Callable:
        def wrapper(handler):
            return self.route(path, "PATCH", handler, before_middleware=before, after_middleware=after)

        return wrapper

    def delete(self,path = None, before = None ,after = None) -> Callable:
        def wrapper(handler):
            return self.route(path, "DELETE", handler, before_middleware=before, after_middleware=after)

        return wrapper

    def include_router(self, routes:dict):
        self.routes = {**self.routes, **routes['routes']}
        self.before_middleware = {**self.before_middleware, **routes['before_middleware']}
        self.after_middleware = {**self.after_middleware, **routes['after_middleware']}

    def ws_route(self, path: str, handler: Callable, before:Callable = None, after:Callable = None) -> None:
        if before is not None:
            self.ws_before[path] = handler

        self.ws_routes[path] = handler

        if after is not None:
            self.ws_after[path] = handler

    def ws(self, path: str , before: Callable = None, after: Callable = None) -> Callable:
        def wrapper(handler: Callable) -> None:
            return self.ws_route(path, handler, before, after)
        return wrapper
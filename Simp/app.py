import inspect
from collections.abc import Callable
from http import HTTPStatus
from typing import Tuple

from .context import Context
from .parse import parse
from .WS_Context import *
import ast

class App:
    def __init__(self):
        self.before_middleware = {}
        self.after_middleware = {}
        self.middlewares = {'before':{}, 'after':{}}
        self.routes = {}
        self.ws_routes = {}
        self.ws_before={}
        self.ws_after={}

    async def __check_func(self, func, ctx):
        result =await func(ctx)
        return True if result is None else False

    async def __call__(self, scope, receive, send):
        # Этот блок кода для отработки lifespan протокола asgi сервера
        if scope['type'] == 'lifespan':
            while True:
                message = await receive()
                if message['type'] == 'lifespan.startup':
                    ...  # Do some startup here!
                    await send({'type': 'lifespan.startup.complete'})
                elif message['type'] == 'lifespan.shutdown':
                    ...  # Do some shutdown here!
                    await send({'type': 'lifespan.shutdown.complete'})
                    return
        #обработка для обработки веб сокета
        elif scope['type'] == 'websocket':
                    while True:
                        event = await receive()
                        ctx = WS_Context(scope, event, send)
                        if event['type'] == 'websocket.connect' or event['type'] == 'websocket.receive':
                            if event['type'] == 'websocket.connect':
                                await ctx.accept()
                            if event['type'] == 'websocket.connect' or event['type'] == 'websocket.receive':
                                await self.ws_get_before(scope['path'], ctx)
                                await self.ws_get_route(scope['path'], ctx)
                                await self.ws_get_after(scope['path'], ctx)
                        elif event['type'] == 'websocket.disconnect' or event['type'] == 'websocket.close':
                            break
        else:
            #Инициализация контекста
            ctx = Context(scope, receive, send)
            #Добавлена обработка ошибок
            #try:
            #Обработка before middleware
            for path, midd_dict in self.before_middleware.items():
                if path == ctx.path():

                    for requst_method, middleware in midd_dict.items():
                        # Сравнение метода обращения и методов, которые есть в словаре(handler_dict)
                        if ctx.method() == requst_method:
                            # Обработка элементов при распарсивании url
                            # Если есть элементы то передаём их в handler
                                # Иначе передаём в хендлер только контекст
                            if await self.__check_func(middleware, ctx):
                                break
                            else:
                                return
                    break

            #Обработка маршрутов по которым обращается пользователь
            for path, handler_dict in self.routes.items():
                    #парсинг именованных параметров в строке запроса
                    #Пример @app.get("/user/{id}")
                    #       async def user(ctx:Context, id):
                    res = parse(path, ctx.path())
                    #Сравнение пути из словаря и пути из запроса
                    #Если они совпадают, то запускается переборка внутреннего словаря(handler_dict) по методам(get, post и т.д)
                    if path == ctx.path():

                        for requst_method, handler in handler_dict.items():
                            #Сравнение метода обращения и методов, которые есть в словаре(handler_dict)
                            if ctx.method() == requst_method:
                                #Обработка элементов при распарсивании url
                                #Если есть элементы то передаём их в handler
                                if res is not None:
                                    await handler(ctx, **res.named)
                                else :
                                #Иначе передаём в хендлер только контекст
                                    await handler(ctx)
                                return

            # Обработка afterMiddleware
            for path, midd_dict in self.after_middleware.items():
                if path == ctx.path():

                    for requst_method, middleware in midd_dict.items():
                        # Сравнение метода обращения и методов, которые есть в словаре(handler_dict)
                        if ctx.method() == requst_method:
                            # Вызов мидлвеера с передачей в него контекста
                            await middleware(ctx)
                            break
                    break
            #Если совпадений нет, то возвращаем ошибку 404
            await ctx.send_body(HTTPStatus.NOT_FOUND, "not found")
            # except Exception as e:
            #     ctx.addHeader("Content-Type", "text/json")
            #     await ctx.send_body(HTTPStatus.INTERNAL_SERVER_ERROR, json.dumps({'error':str(e)}))


    #Базовая функция маршрутизации
    def route(self, path: str, method: str, handler , before_middleware = None, after_middleware = None) -> Callable:
        # переменная для маршрутизации (По пути который передаём либо от названия хендлера)
        path_name = path or f"/{handler.__name__}"

        if path_name not in self.routes:
            self.routes[path_name] = {}

        self.routes[path_name][method] = handler

        if before_middleware is not None or after_middleware is not None:
            self.before_middleware[path_name] = {}
            self.before_middleware[path_name][method] = before_middleware

        if after_middleware is not None or after_middleware is not None:
            self.after_middleware[path_name] = {}
            self.after_middleware[path_name][method] = before_middleware

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
        self.ws_routes = {**self.ws_routes, **routes['ws_routes']}
        self.ws_after = {**self.ws_after, **routes['ws_after']}
        self.ws_before = {**self.ws_before, **routes['ws_before']}
        self.routes = {**self.routes, **routes['routes']}
        self.before_middleware = {**self.before_middleware, **routes['before_middleware']}
        self.after_middleware = {**self.after_middleware, **routes['after_middleware']}

    #Функция, которая копирует путь в json файл
    def get_route(self, file:str):
        routes = self.routes.items()
        total = b""

        f = open(file, '+wb')
        f.write(b'{\n')
        for route in routes:
            for method in route[1]:
                string = bytes('\t"' + method + '" : "' + route[0] + '",\n', encoding='utf-8')
                total += string

        total = total[:-2]
        total += b'\n'
        f.write(total)
        f.write(b'}')
        f.close()

    async def ws_get_before(self, path: str, ctx: WS_Context):
        for route in self.ws_before:
            if path == route:
                    handler = self.ws_before[route]
                    return await handler(ctx)
            return await self.notFoundHandler(ctx)

    async def ws_get_after(self, path: str, ctx: WS_Context):
        for route in self.ws_after:
            if path == route:
                    handler = self.ws_after[route]
                    return await handler(ctx)
            return await self.notFoundHandler(ctx)

    async def ws_get_route(self, path: str, ctx: WS_Context):
        for route in self.ws_routes:
            if path == route:
                    handler = self.ws_routes[route]
                    return await handler(ctx)
            return await self.notFoundHandler(ctx)

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

    async def notFoundHandler(self, ctx: WS_Context):
        await ctx.send_message('Not Found')
        await ctx.close()

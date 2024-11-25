from collections.abc import Callable
from http import HTTPStatus
from Framework.context import Context
from Framework.parse import parse

class Simp:
    def __init__(self):
        self.middlewares = {'before':{}, 'after':{}}
        self.routes = {}

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
        else:
            #Инициализация контекста
            ctx = Context(scope, receive, send)

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
            #Если совпадений нет, то возвращаем ошибку 404
            await ctx.send_body(HTTPStatus.NOT_FOUND, "not found")



    #Базовая функция маршрутизации
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

    def include_router(self, routes:dict):
        self.routes = {**self.routes, **routes}


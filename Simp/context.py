from http import HTTPStatus
from typing import Any
from warnings import catch_warnings

# Класс для удобной обработки запросов, вдохновлён gin Context в Golang
class Context:
    def __init__(self, scope, receive, send):
        self.scope = scope
        self.receive = receive
        self.send = send
        self.headers = []
        self.cookies = self._get_cookies()

    def getScope(self):
        return self.scope

    def type(self):
        return self.scope['type']

    def asgi(self):
        return self.scope['asgi']

    def http_version(self):
        return self.scope['http_version']

    def client(self):
        return self.scope['client']

    def server(self):
        return self.scope['server']

    def scheme(self):
            return self.scope['scheme']
    def method(self):
        return self.scope['method']

    def root_path(self):
        return self.scope['root_path']

    def path(self):
        return self.scope['path']

    def query_params(self):
        params = {}
        query_string = str(self.scope['query_string'])
        query_string = query_string.replace("b", '', 1)
        query_string = query_string.replace("'", '', 2)
        if query_string:
            req_queries = query_string.split('&')

            for query in req_queries:
                query_key, query_val = query.split("=")

                params[query_key] = query_val
        return params

    def getHeaders(self):
        return self.scope['headers']

    def state(self):
        return self.scope['state']

    def _get_cookies(self):
        headers = self.scope['headers']
        cookies = {}
        for header in headers:
            if header[0] == b'cookie':
                cooka = str(header[1])
                cooka = cooka.replace('b', '', 2)
                cooka = cooka.replace("'", '', 2)
                cooka = cooka.split(";")
                for cook in cooka:
                    (key, value) = cook.split("=")
                    cookies[key.lstrip()] = value.lstrip()
        return cookies

    def addCookie(self, name:str, value:str, expires:float=None, Secure:bool = False, HttpOnly:bool = False):
        cookieSTR = name+"="+value+";"

        if expires is not None:
            cookieSTR = cookieSTR+"Max-Age="+str(int(expires))+";"

        if HttpOnly:
            cookieSTR = cookieSTR+"HttpOnly;"

        if Secure:
            cookieSTR = cookieSTR+"Secure;"
        cookie = ('Set-Cookie', cookieSTR)
        self.headers.append(cookie)

    async def body(self):
        return await self.receive()

    def addHeader(self, name, value):
        self.headers.append((name,value))

    async def send_body(self, status: HTTPStatus = HTTPStatus.NOT_FOUND, body:Any = None):
        try:
            await self.send({
                'type': 'http.response.start',
                'status': status,
                'headers': self.headers,
            })

            await self.send({
                'type': 'http.response.body',
                'body': bytes(body, 'utf-8'),
            })
        except Exception as e:
            print(e)

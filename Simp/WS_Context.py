from asyncio import Task

from Tools.scripts.make_ctype import method


class WS_Scope:
     def __init__(self, scope):
         try:
             self.type = scope['type']
             self.asgi = scope['asgi']
             self.http_version = scope['http_version']
             self.scheme = scope['scheme']
             self.server = scope['server']
             self.client = scope['client']
             self.root_path = scope['root_path']
             self.path = scope['path']
             self.query_string = scope['query_string']
             self.headers = scope['headers']
             self.subprotocols = scope['subprotocols']
             self.state = scope['state']
             self.extensions = scope['extensions']
         except KeyError as e:
             print(e)


class WS_Send:
    def __init__(self, send: method):
        self.send: method = send

    async def accept(self, subprotocol=None):
        """Accept the WebSocket connection."""
        await self.send({
            'type': 'websocket.accept',
            'subprotocol': subprotocol
        })

    async def close(self, code=None):
        """Close the WebSocket connection."""
        await self.send({
            'type': 'websocket.close',
            'code': code
        })


    async def send_message(self, message):
        """Send a message through the WebSocket connection."""
        if isinstance(message, str):
            await self.send({
                'type': 'websocket.send',
                'text': message
            })
        elif isinstance(message, bytes):
            await self.send({
                'type': 'websocket.send',
                'bytes': message
            })
        else:
            raise ValueError("Message must be of type str or bytes")


class WS_Context:
    def __init__(self, scope: dict, event: dict, send: method):
        self.scope: WS_Scope= WS_Scope(scope)
        self.event = event
        self.send: WS_Send = WS_Send(send)

    async def accept(self, subprotocol=None):
        """Accept the WebSocket connection."""
        await self.send.accept(subprotocol)

    async def close(self, code=1000):
        """Close the WebSocket connection."""
        await self.send.close(code)

    async def send_message(self, message):
        """Send a message through the WebSocket connection."""
        await self.send.send_message(message)


    async def receive_message(self):
        """Receive a message from the WebSocket connection."""
        event = self.event
        if event['type'] == 'websocket.receive':
            return event.get('text', None) or event.get('bytes', None)
        elif event['type'] == 'websocket.disconnect':
            raise ConnectionClosed(event['code'])


class ConnectionClosed(Exception):
    """Exception raised when the WebSocket connection is closed."""
    def __init__(self, code):
        self.code = code
        super().__init__(f"WebSocket connection closed with code: {code}")
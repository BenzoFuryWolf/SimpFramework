# Simp framework

Это небольшой фреймворк с поддержкой протоколов http, ws

Пример использования с протоколом http
```
    import uvicorn

    from http import HTTPStatus
    from Simp.app import App
    from Simp.context import Context

    app = App()

    @app.get("/")
    async def ind(ctx: Context):
        await ctx.send_body(HTTPStatus.OK, "Hello World")

    uvicorn.run(app, host="127.0.0.1", port=4400)
```

Пример с использования с протоколом websocket
```
    import uvicorn
    import Simp

    #Инициализация приложения
    app = Simp.App()
    #массив где хранятся все сообщения полученные от пользователей
    messages = []

    @app.ws('/ap')
    async def handler(ctx: Simp.WS_Context):
        #Получение сообщения от пользователя из канала
        message =await ctx.receive_message()
        #Получение доступа к глобальному массиву messages
        global messages
        #Если сообщение пустое, то его не записываем в массив
        if message is not None:
            messages.append(message)
        #Конвертация в json массива сообщений
        message = json.dumps(messages)
        #Вывод ответа пользователю
        print(f"Received message: {message}")
        #Отправка сообщения клиенту
        await ctx.send_message(message)

    #Запуск веб сервера
    uvicorn.run(app, host="127.0.0.1", port=8000, ws='websockets')
```

Он использует парсер из github
Ссылка:
https://github.com/r1chardj0n3s/parse
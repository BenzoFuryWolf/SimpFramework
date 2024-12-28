# Класс Context

### Методы класса `Context`

#### 1. **`__init__(self, scope, receive, send)`**

Инициализирует объект `Context`.
##### Аргументы:

- `scope`: словарь, содержащий метаданные соединения (например, заголовки, метод, путь, параметры).
- `receive`: функция для получения данных из запроса.
- `send`: функция для отправки ответа клиенту.

##### Описание:

Инициализирует контекст для обработки HTTP-запроса и ответа, включая заголовки и куки.

##### Пример:
```
async def app(scope, receive, send):
	#Создание контекста
	ctx = Context(scope, receive, send)
	#Передача контекста в обработчик
	await handler(ctx)
```

---

#### 2. **`getScope(self)`**

Возвращает текущий `scope`.

##### Возвращаемое значение:

- Объект `scope` (словарь).

##### Описание:

Предоставляет доступ к исходным данным о запросе.

##### Пример:
```
scope = ctx.getScope()
print(scope)
```

---

#### 3. **`type(self)`**

Возвращает тип соединения (например, `http` или `websocket`).

##### Возвращаемое значение:

- Тип соединения из `scope['type']`.

##### Пример:
```
connection_type = context.type() 
print(f"Connection type: {connection_type}")
```

---

#### 4. **`asgi(self)`**

Возвращает спецификацию ASGI.

##### Возвращаемое значение:

- Данные из `scope['asgi']`.

##### Пример:
```
asgi_version = context.asgi() 
print(f"ASGI version: {asgi_version}")
```

---

#### 5. **`http_version(self)`**

Возвращает версию HTTP.
##### Возвращаемое значение:
- строку `(версия)`.
##### Пример:
```
version = context.http_version() 
print(f"HTTP version: {version}")
````

---

#### 6. **`client(self)`**

Возвращает данные о клиенте.
##### Возвращаемое значение:

- Кортеж `(ip, порт)`.
##### Пример:
```
client_info = context.client()
print(f"Client IP: {client_info[0]}")
```
---

#### 7. **`server(self)`**

Возвращает данные о сервере.
##### Пример:
```
server_info = context.server() 
print(f"Server address: {server_info}")
```

---

#### 8. **`scheme(self)`**

Возвращает протокол соединения (например, `http` или `https`).
##### Пример:
```
protocol = context.scheme() 
print(f"Connection scheme: {protocol}")
```

---

#### 9. **`method(self)`**

Возвращает HTTP-метод запроса (например, `GET`, `POST`).
##### Пример:

```
http_method = context.method() 
print(f"HTTP method: {http_method}")
```

---

#### 10. **`root_path(self)`**

Возвращает корневой путь приложения.
##### Пример:
```
root_path = context.root_path() 
print(f"Root path: {root_path}")
```

---

#### 11. **`path(self)`**

Возвращает путь запроса.
##### Пример:
```
request_path = context.path() 
print(f"Request path: {request_path}")
```

---

#### 12. **`query_params(self)`**

Возвращает параметры запроса в виде словаря.
##### Пример:
```
params = context.query_params() 
print(params)
```

---

#### 13. **`getHeaders(self)`**

Возвращает заголовки запроса.
##### Пример:
```
headers = context.getHeaders() 
print(headers)
```

---

#### 14. **`state(self)`**

Возвращает состояние `scope`.

##### Пример:

```
state = context.state() 
print(state)
```

---

#### 15. **`_get_cookies(self)`**

Парсит и возвращает куки из заголовков.
##### Пример:

```
cookies = context.cookies 
print(cookies)
```
---

#### 16. **`addCookie(self, name, value, expires=None, Secure=False, HttpOnly=False, path="/")`**

Добавляет cookie в заголовки ответа.

##### Пример:
`context.addCookie("session_id", "abc123", expires=3600, HttpOnly=True)`

---

#### 17. **`body(self)`**

Возвращает тело запроса.
##### Пример:
```
data = await context.body() 
print(data)
```
---

#### 18. **`addHeader(self, name, value)`**
Добавляет заголовок в HTTP-ответ.
##### Пример:
`context.addHeader("X-Custom-Header", "Value")`

---

#### 19. **`send_body(self, status, body)`**

Отправляет HTTP-ответ клиенту.
##### Пример:
`await context.send_body(HTTPStatus.OK, "Response body")`

# Примеры использования
#### Пример 1: Обработка GET-запроса с параметрами
```
@app.get('/')
async def handle_get_request(context):     
	params = context.query_params()     
	response = {"status": "success", "data": params}     
	await context.send_body(
							HTTPStatus.OK, 
							json.dumps(response)
							)
```

#### Пример 2: Чтение параметров запроса и отправка cookie

```
@app.get('/cookie')
async def handle_get_with_cookie(context): 

	# Получаем параметры запроса     
	params = context.query_params()  
	    
	# Читаем cookie из запроса     
	user_cookie = context.cookies.get("user_id")  
	   
	if not user_cookie:         
	# Устанавливаем cookie, если его нет     
	    
		context.addCookie("user_id", "12345", HttpOnly=True, Secure=True)    
		  
	response = {         
		"status": "success",         
		"params": params,         
		"message": f"User cookie: {
		user_cookie or 'New cookie set'
		}"     
	}  
	        
	# Отправляем HTTP-ответ     
	await context.send_body(
							HTTPStatus.OK, 
							json.dumps(response)
							)
```
---

#### Пример 3: Установка нескольких cookie и отправка их клиенту

```
@app.get('/get-cookie')
async def handle_set_cookies(context):     
	# Устанавливаем cookie     
	context.addCookie(
						"session_token", 
						"abc123", 
						expires=3600, 
						HttpOnly=True, 
						Secure=True
					)     
					
	context.addCookie("theme", "dark", expires=86400, path="/")      
	# Формируем ответ     
	
	response = {"message": "Cookies set successfully"}          
	# Отправляем ответ с заголовками cookie     
	await context.send_body(HTTPStatus.OK, json.dumps(response))
```
---

#### Пример 4: Обновление и удаление cookie

```
async def handle_update_and_remove_cookie(context):  

	# Обновляем cookie     
	context.addCookie("session_token", 
					  "new_token_value", 
					   expires=7200, 
					   HttpOnly=True
					   )   
					      
	# Удаляем cookie (устанавливаем отрицательное время жизни)  
	context.addCookie(
						"theme",
						 "", 
						 expires=-1
					)     
	 
	response = {   
			"message": "Cookie updated and theme cookie removed"     
				}  
				        
	await context.send_body(HTTPStatus.OK, json.dumps(response))
```

---

#### Пример 5: Чтение и вывод cookie в ответе

```
async def handle_read_cookies(context):     
	# Получаем все cookie     
	cookies = context.cookies      
	response = {         
		"message": "Retrieved cookies",         
		"cookies": cookies     
	}         
	await context.send_body(HTTPStatus.OK, json.dumps(response))
```

#### Пример 6: Обработка POST-запроса с телом
```
async def handle_post_request(context):     
	data = await context.body()     
	print(data)     
	await context.send_body(HTTPStatus.CREATED, "Data received")
```


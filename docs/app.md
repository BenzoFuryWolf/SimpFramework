# Класс App

### Методы класса `App`

#### 1. **`__init__(self)`**

Инициализация объекта `App`.

##### Описание:

- Инициализирует словари для хранения маршрутов (`routes`) и middleware (`before_middleware`, `after_middleware`).
- `before_middleware` и `after_middleware` разделены для обработки запросов до и после основного обработчика.

##### Пример:
```
import Simp

app = Simp.App()
```

---

#### 2. **`__check_func(self, func, ctx)`**

Вспомогательный метод для вызова middleware.

##### Аргументы:

- `func`: Middleware-функция.
- `ctx`: Объект контекста `Context`.

##### Возвращаемое значение:

- `True`, если middleware завершилось успешно (возвращает `None`), иначе `False`.

##### Пример:

```
#обработка словаря с middlewares
for path, midd_dict in self.before_middleware.items():  
    #если такой путь есть в словаре 
    if path == ctx.path():  
  
        for requst_method, middleware in midd_dict.items():  
        
# Сравнение метода обращения и методов, которые есть в словаре (handler_dict)    
            if ctx.method() == requst_method:  
            
                if await self.__check_func(middleware, ctx):  
	                
	                #Выходит из цикла
                    break  
                    
                else:  
                
		            #Останавливает функцию
                    return  
                    
        #Выходит из цикла
        break
```

---

#### 3. **`__call__(self, scope, receive, send)`**

Главный метод для обработки ASGI-запросов.

##### Аргументы:

- `scope`: Словарь с метаданными запроса.
- `receive`: Функция для получения данных запроса.
- `send`: Функция для отправки ответа.

##### Описание:

- Если тип `scope['type']` равен `lifespan`, обрабатываются события запуска и завершения приложения.
- Для HTTP-запросов:
    - Инициализируется контекст `Context`.
    - Обрабатываются middleware до (`before_middleware`) и после (`after_middleware`) маршрута.
    - Маршрут и его обработчик определяются на основе пути и HTTP-метода.

##### Пример:

```
import Simp
import uvicorn

app = Simp.App()

uvicorn.run(app, host="127.0.0.1", port=4500)
```

---

#### 4. **`route(self, path, method, handler, before_middleware=None, after_middleware=None)`**

Регистрирует маршрут с обработчиком и middleware.

##### Аргументы:

- `path`: Путь запроса.
- `method`: HTTP-метод.
- `handler`: Функция-обработчик.
- `before_middleware`: Middleware, выполняемый перед обработчиком.
- `after_middleware`: Middleware, выполняемый после обработчика.

##### Пример:
```
def my_handler(ctx):     
	print("Handler executed")  
	app.route("/home", "GET", my_handler)`
```


---

#### 5. **`get(self, path=None, before=None, after=None)`**

Декоратор для регистрации маршрута с методом `GET`.

##### Пример:
```
@app.get("/welcome") 
async def welcome_handler(ctx):     
	await ctx.send_body(200, "Welcome!")
```


---

#### 6. **`post(self, path=None, before=None, after=None)`**

Декоратор для регистрации маршрута с методом `POST`.

##### Пример:

```
@app.post("/submit") 
async def submit_handler(ctx):     
	data = await ctx.body()     
	print(data)
```

---

#### 7. **`put(self, path=None, before=None, after=None)`**

Декоратор для регистрации маршрута с методом `PUT`.

##### Пример:

python

Копировать код

```
@app.put("/update") 
async def update_handler(ctx):     
	print("Update requested")
```

---

#### 8. **`patch(self, path=None, before=None, after=None)`**

Декоратор для регистрации маршрута с методом `PATCH`.

##### Пример:
```
@app.patch("/modify") 
async def modify_handler(ctx):     
	print("Modify requested")
```

---

#### 9. **`delete(self, path=None, before=None, after=None)`**

Декоратор для регистрации маршрута с методом `DELETE`.

##### Пример:
```
@app.delete("/remove") 
async def remove_handler(ctx):     
	print("Remove requested")
```

---

#### 10. **`include_router(self, routes)`**

Добавляет маршруты из другого объекта `Simp`.

##### Аргументы:

- `routes`: Словарь с маршрутами и middleware.

##### Пример:
```
sub_routes = {     

	"routes": {"/api": {"GET": my_handler}},     
	"before_middleware": {},     
	"after_middleware": {} 
	}  
	
app.include_router(sub_routes)
```

---

#### 11. **`get_route(self, file)`**

Сохраняет список маршрутов в JSON-файл.

##### Аргументы:

- `file`: Имя файла для сохранения.

##### Пример:

```
import Simp
import json
import uvicorn
from http import HTTPStatus

app = Simp.App()

@app.get('/api')
async def api(ctx: Simp.Context):
	ctx.send_body(
		HTTPStatus.OK,
		json.dumps({'status':'ok'})
	)

app.get_route("routes.json")

uvicorn.run(app, host="127.0.0.1", port=4500)

```
---
### Примеры использования

#### Пример 1: Регистрация маршрута с middleware

@app.get("/hello", before=lambda ctx: print("Before middleware executed")) async def hello_handler(ctx):     await ctx.send_body(200, "Hello, world!")

#### Пример 2: Работа с маршрутами и контекстом

```
@app.post("/submit") 
async def submit_handler(ctx):     
	data = await ctx.body()     
	print(f"Received data: {data}")     
	await ctx.send_body(200, "Data received")
````

#### Пример 3: Интеграция middleware для POST-запросов

```
async def log_request(ctx):     
	print(f"Request path: {ctx.path()}")  
	
@app.post("/log", before=log_request) 
async def log_handler(ctx):     
	await ctx.send_body(200, "Request logged")
	
```

---
### Заключение

Класс `App` предоставляет гибкий механизм маршрутизации и управления middleware, что делает его идеальным для разработки ASGI-приложений. Благодаря декораторам и поддержке именованных параметров, разработка маршрутов становится интуитивно понятной.

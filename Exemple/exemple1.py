import json
import datetime
import uvicorn

from http import HTTPStatus
from Simp.app import Simp
from Simp.context import Context

app = Simp()

@app.get("/")
async def ind(ctx: Context):
    await ctx.send_body(HTTPStatus.OK, "Hello World")


@app.get("/app")
async def lll(ctx: Context):

    ctx.addHeader('Content-type', 'text/json')
    await ctx.send_body(HTTPStatus.OK,json.dumps({'msg':'success'}))

# Пример как задать cookies
@app.get("/cookies")
async def cookies(ctx: Context):
    expires = datetime.timedelta(days=1).total_seconds()
    ctx.addHeader('Content-type', 'text/json')
    ctx.addCookie("id", "6", expires=expires, HttpOnly=True)
    ctx.addCookie("token", "token", expires=expires, HttpOnly=True)
    await ctx.send_body(HTTPStatus.OK,json.dumps({'msg':'success'}))

#Пример получения cookies
@app.get("/getCookies")
async def getCookies(ctx: Context):
    ctx.addHeader('Content-type', 'text/json')
    await ctx.send_body(HTTPStatus.OK,json.dumps(ctx.cookies))

uvicorn.run(app, host="127.0.0.1", port=4400, lifespan="on")
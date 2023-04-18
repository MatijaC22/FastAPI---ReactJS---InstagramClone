# INTRO
# YOU CAN HOST IS ON FREE HOSTING SERVICE CALLED "DETA" - ITS MADE FOR HOSTING FASTAPI
# ACCESS TOKEN FOR DETA SPACE -> mNkFztY6_uHh3dscLWiZ1K2CYgTS7n6MFUY6hF55E

from fastapi import FastAPI, Request, HTTPException
from router import blog_get, blog_post, user, article, product, file
from auth import authentication
from db import models
from db.database import engine
from exceptions import StoryException
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from templates import templates
import time 
from client import html
from fastapi.websockets import WebSocket

app = FastAPI()
app.include_router(templates.router)
app.include_router(authentication.router)
app.include_router(file.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)
    
@app.get('/hello')
def index():
    return {"message":'hello world!'}


@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(
        status_code = 418,
        content = {'detail': exc.name}
    )


@app.get("/")
async def get():
    return HTMLResponse(html)

clients = []

@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    while True:
        data = await websocket.recieve_text()
        for client in clients:
            await client.send_text(data)

# @app.exception_handler(HTTPException)
# def custom_handler(request: Request, exc: StoryException):
#     return PlainTextResponse(str(exc), status_code = 400)

@app.middleware("http")
async def add_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers['duration'] = str(duration)
    return response


origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

models.Base.metadata.create_all(engine)


# da se omoguci uci u files folder s browsera i vidjeti slike
app.mount('/files', StaticFiles(directory='files'), name='files')
app.mount('/templates/static', StaticFiles(directory='templates/static'), name='static')
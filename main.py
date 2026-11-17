from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi import Request

from app.api.routes import router
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(router)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

templates = Jinja2Templates(
    directory="app/templates"
)

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )
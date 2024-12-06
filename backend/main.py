from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from . import models, database, oauth2
from .routers import translate, authorize, profile

app = FastAPI(title="AI Translate", version="1.0.0")
models.Base.metadata.create_all(bind=database.engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)

templates = Jinja2Templates(directory="frontend")
app.mount("/static", StaticFiles(directory="frontend/src"), name="static")

app.include_router(translate.router)
app.include_router(authorize.router)
app.include_router(profile.router)


@app.get("/", response_class=HTMLResponse, tags=["Frontend"])
async def index(request: Request, response: Response):
    try:
        oauth2.require_login(request)
    except HTTPException:
        return RedirectResponse(url="/authorize", status_code=302)

    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/authorize", response_class=HTMLResponse, tags=["Frontend"])
async def authorize(request: Request):
    return templates.TemplateResponse("authorize.html", {"request": request})


@app.get("/signup", response_class=HTMLResponse, tags=["Frontend"])
async def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.routes import users

app = FastAPI()
app.title = "BACKEND TEST"
app.version = "0.0.1"
app.description = "A simple user API."

app.include_router(users.router)


@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse("/docs")

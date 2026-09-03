# para rodar o código no terminal: uvicorn main:app --reload

import os

from dotenv import load_dotenv
from fastapi import FastAPI

from routes.auth import router as auth_router
from routes.orders import router as order_router

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()

app.include_router(auth_router)
app.include_router(order_router)

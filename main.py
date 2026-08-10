# para rodar o código no terminal: uvicorn main:app --reload

from fastapi import FastAPI

from routes.auth import router as auth_router
from routes.order import router as order_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(order_router)

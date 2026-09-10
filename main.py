# para rodar o código no terminal: uvicorn main:app --reload
from fastapi import FastAPI

from routes.auth import router as auth_router
from routes.orders import router as order_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(order_router)


@app.get("/")
def root():
    return {"mensagem": "Bem-vindo à API de autenticação e pedidos!"}

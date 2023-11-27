import uvicorn
from fastapi import FastAPI
from routers import clients, pet, consultation
from db import database

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(clients.router, tags=["clients"])
app.include_router(pet.router, tags=["pets"])
app.include_router(consultation.router, tags=["consultations"])

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )

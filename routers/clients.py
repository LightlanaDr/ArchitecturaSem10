from datetime import datetime

from fastapi import APIRouter, HTTPException
from db import clients, database
from models import Client, ClientIn

router = APIRouter()


@router.get("/clients/", response_model=list[Client])
async def get_all():
    result = clients.select()
    return await database.fetch_all(result)


@router.get("/clients/{client_id}", response_model=Client)
async def get_by_id(client_id: int):
    result = clients.select().where(clients.c.id == client_id)
    fetch = await database.fetch_one(result)
    if not fetch:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    return fetch


@router.post("/clients/", response_model=Client)
async def create(client: ClientIn):
    now = datetime.now().date().year
    if now - client.birthday.year > 18:
        result = clients.insert().values(document=client.document,
                                         surName=client.surName,
                                         firstName=client.firstName,
                                         patronymic=client.patronymic,
                                         birthday=client.birthday)
        last_record_id = await database.execute(result)
        return {**client.model_dump(), "id": last_record_id}
    else:
        raise HTTPException(status_code=404, detail='Возраст не может быть меньше 18 лет')


@router.put("/clients/{client_id}", response_model=Client)
async def update(client_id: int, new_client: ClientIn):
    result = clients.update().where(clients.c.id == client_id).values(**new_client.model_dump())
    fetch = await database.execute(result)
    if not fetch:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    return {**new_client.model_dump(), "id": client_id}


@router.delete("/clients/{client_id}")
async def delete(client_id: int):
    result = clients.delete().where(clients.c.id == client_id)
    fetch = await database.execute(result)
    if not fetch:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    return {'message': 'Пользователь удален'}

from fastapi import APIRouter, HTTPException
from db import database, consultations
from models import Consultation, ConsultationIn

router = APIRouter()


@router.get("/consultations/", response_model=list[Consultation])
async def get_all():
    query = consultations.select()
    return await database.fetch_all(query)


@router.get("/consultations/{consultation_id}", response_model=Consultation)
async def get_by_id(consultation_id: int):
    result = consultations.select().where(consultations.c.id == consultation_id)
    fetch = await database.fetch_one(result)
    if not fetch:
        raise HTTPException(status_code=404, detail='Консультация не найдена')
    return fetch


@router.post("/consultations/", response_model=Consultation)
async def create(consultation: ConsultationIn):
    result = consultations.insert().values(clientId=consultation.clientId,
                                          petId=consultation.petId,
                                          consultationDate=consultation.consultationDate,
                                          description=consultation.description)
    last_record_id = await database.execute(result)
    return {**consultation.model_dump(), "id": last_record_id}


@router.put("/consultations/{consultation_id}", response_model=Consultation)
async def update(consultation_id: int, new_consultation: ConsultationIn):
    result = consultations.update().where(consultations.c.id == consultation_id).values(**new_consultation.model_dump())
    fetch = await database.execute(result)
    if not fetch:
        raise HTTPException(status_code=404, detail='Консультация не найдена')
    return {**new_consultation.model_dump(), "id": consultation_id}


@router.delete("/consultations/{consultation_id}")
async def delete(consultation_id: int):
    query = consultations.delete().where(consultations.c.id == consultation_id)
    fetch = await database.execute(query)
    if not fetch:
        raise HTTPException(status_code=404, detail='Consultation not found')
    return {'message': 'Консультация удалена'}
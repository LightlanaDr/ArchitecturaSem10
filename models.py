import datetime

from pydantic import BaseModel


class Client(BaseModel):
    id: int
    document: str
    surName: str
    firstName: str
    patronymic: str
    birthday: datetime.date


class ClientIn(BaseModel):
    document: str
    surName: str
    firstName: str
    patronymic: str
    birthday: datetime.date


class Consultation(BaseModel):
    id: int
    clientId: int
    petId: int
    consultationDate: datetime.date
    description: str


class ConsultationIn(BaseModel):
    clientId: int
    petId: int
    consultationDate: datetime.date
    description: str


class Pet(BaseModel):
    id: int
    clientId: int
    name: str
    pet_birthday: datetime.date


class PetIn(BaseModel):
    clientId: int
    name: str
    pet_birthday: datetime.date

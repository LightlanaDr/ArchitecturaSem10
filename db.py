import databases
import sqlalchemy

metadata = sqlalchemy.MetaData()

clients = sqlalchemy.Table(
    "clients",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.INTEGER, primary_key=True),
    sqlalchemy.Column("document", sqlalchemy.String),
    sqlalchemy.Column("surName", sqlalchemy.String),
    sqlalchemy.Column("firstName", sqlalchemy.String),
    sqlalchemy.Column("patronymic", sqlalchemy.String),
    sqlalchemy.Column("birthday", sqlalchemy.Date),
)

pets = sqlalchemy.Table(
    "pets",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.INTEGER, primary_key=True),
    sqlalchemy.Column("clientId", sqlalchemy.ForeignKey("clients.id")),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("pet_birthday", sqlalchemy.Date),

)

consultations = sqlalchemy.Table(
    "consultations",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.INTEGER, primary_key=True),
    sqlalchemy.Column("clientId", sqlalchemy.ForeignKey("clients.id")),
    sqlalchemy.Column("petId", sqlalchemy.ForeignKey("pets.id")),
    sqlalchemy.Column("consultationDate", sqlalchemy.Date),
    sqlalchemy.Column("description", sqlalchemy.String),
)

DATABASE_URL = "sqlite:///./ClinicService.db"

database = databases.Database(DATABASE_URL)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)


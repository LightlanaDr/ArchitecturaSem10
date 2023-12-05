import databases
import pytest
import sqlalchemy
from sqlalchemy_utils import drop_database, create_database

metadata = sqlalchemy.MetaData()
TEST_DB_URL = "sqlite:///test.db"
fake_db = databases.Database(TEST_DB_URL)
engine = sqlalchemy.create_engine(
    TEST_DB_URL, connect_args={"check_same_thread": False}
)


@pytest.fixture(scope="module")
def temp_db():
    create_database(TEST_DB_URL)
    try:
        yield TEST_DB_URL
    finally:
        drop_database(TEST_DB_URL)

from contextlib import contextmanager
from collections.abc import Iterator
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from google.cloud.sql.connector import Connector


PROJECT_ID = "magnetic-lore-403609"
REGION = "europe-west4"
INSTANCE_NAME = "dragon-data"
INSTANCE_CONNECTION_NAME = f"{PROJECT_ID}:{REGION}:{INSTANCE_NAME}"
DB_USER = "root"
DB_PASS = "C$ca7radragondata"
DB_NAME = "dragon_database"

connector = Connector()


def get_pool() -> Engine:
    return create_engine("mysql+pymysql://", creator=get_connection)

def db_url() -> str:
    return "mysql+pymysql://"

def get_connection():
    connection = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME,
        port=3306,
    )
    return connection

SessionMaker = sessionmaker(bind=create_engine(db_url(), creator=get_connection))
@contextmanager
def session_from_env() -> Iterator[Session]:
    with SessionMaker(expire_on_commit=False) as session:
        try:
            yield session
        except:
            session.rollback()
            raise
        else:
            session.commit()
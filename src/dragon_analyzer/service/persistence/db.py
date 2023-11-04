from sqlalchemy.orm import Session

from dragon_analyzer.database.orm.db import Base

def init_db_tables(db_session: Session):
    Base.metadata.create_all(db_session.get_bind())

def clean_db_tables(db_session: Session):
    db_session.delete()
    db_session.commit()

def clean_and_init_db_tables(db_session: Session):
    db_session.delete()

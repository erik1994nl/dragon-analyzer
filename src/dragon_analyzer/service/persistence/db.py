from sqlalchemy import select
from sqlalchemy.orm import Session
from dragon_analyzer.database.orm.speed_coach import SessionSummaryDb

from dragon_analyzer.database.orm.db import Base
from dragon_analyzer.speedcoach.reader import SpeedData

def init_db_tables(db_session: Session):
    Base.metadata.create_all(db_session.get_bind())

def clean_db_tables(db_session: Session):
    db_session.delete()
    db_session.commit()

def clean_and_init_db_tables(db_session: Session):
    db_session.delete()

def get_session_summary_data(db_session: Session) -> SpeedData:
    statement = select(SessionSummaryDb)
    session_summary = db_session.execute(statement).scalar()
    if not session_summary:
        raise ValueError("No session summary found.")
    return session_summary

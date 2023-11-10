from fastapi import FastAPI
# from plot import plot_speed_data
from dragon_analyzer.service.persistence.db import clean_and_init_db_tables, clean_db_tables, get_session_summary_data, init_db_tables
from dragon_analyzer.service.persistence.speed_coach import persist_speed_data
from dragon_analyzer.database.db import session_from_env

from dragon_analyzer.speedcoach.reader import read_data, read_data_data_frame

app = FastAPI(
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
)

@app.post("/api/speed-data/persist")
def post_persist_speed_data():
    speed_data = read_data()
    with session_from_env() as db_session:
        persist_speed_data(db_session, speed_data)

@app.post("/api/init-db-tables")
def post_init_db_tables():
    with session_from_env() as db_session:
        init_db_tables(db_session)

@app.post("/api/clean-db-tables")
def post_clean_db_tables():
    with session_from_env() as db_session:
        clean_db_tables(db_session)

@app.post("/api/clean-and-init-db-tables")
def post_clean_and_init_db_tables():
    with session_from_env() as db_session:
        clean_and_init_db_tables(db_session)

@app.get("/api/speed-data")
def get_session_summary():
    print("GETTING FOR DRAGON USER!")
    with session_from_env() as db_session:
        return get_session_summary_data(db_session)

# speed_data_data_frame = read_data_data_frame()

# plot_speed_data(speed_data)

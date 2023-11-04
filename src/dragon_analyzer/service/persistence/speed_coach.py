from dragon_analyzer.database.orm.speed_coach import IntervalSummaryDb, PerStrokeDataDb, SessionSummaryDb
from dragon_analyzer.speedcoach.interval_summary import IntervalSummary
from dragon_analyzer.speedcoach.per_stroke_data import PerStrokeData
from dragon_analyzer.speedcoach.reader import SpeedData
from dragon_analyzer.speedcoach.session_summary import SessionSummary
from sqlalchemy.orm import Session
from collections.abc import Collection

def build_session_summary_db(session_summary: SessionSummary) -> SessionSummaryDb:
    return SessionSummaryDb(
        intervals=session_summary.intervals,
        distance=session_summary.distance,
        distance_imp=session_summary.distance_imp,
        total_elapsed_time=session_summary.total_elapsed_time,
        avg_split=session_summary.avg_split,
        avg_speed=session_summary.avg_speed,
        avg_split_imp=session_summary.avg_split_imp,
        avg_speed_imp=session_summary.avg_speed_imp,
        avg_stroke_rate=session_summary.avg_stroke_rate,
        total_strokes=session_summary.total_strokes,
        distance_per_stroke=session_summary.distance_per_stroke,
        distance_per_stroke_imp=session_summary.distance_per_stroke_imp,
        avg_heart_rate=session_summary.avg_heart_rate,
        avg_cal_per_hr=session_summary.avg_cal_per_hr,
        total_cals=session_summary.total_cals,
        start_gps_lat=session_summary.start_gps_lat,
        start_gps_lon=session_summary.start_gps_lon,
    )

def build_interval_summary_db(interval_summary: IntervalSummary, session_id: int) -> IntervalSummaryDb:
    return IntervalSummaryDb(
        session_id=session_id,
        interval=interval_summary.interval,
        total_distance=interval_summary.total_distance,
        total_distance_imp=interval_summary.total_distance_imp,
        total_elapsed_time=interval_summary.total_elapsed_time,
        avg_split=interval_summary.avg_split,
        avg_speed=interval_summary.avg_speed,
        avg_split_imp=interval_summary.avg_split_imp,
        avg_speed_imp=interval_summary.avg_speed_imp,
        avg_stroke=interval_summary.avg_stroke,
        total_strokes=interval_summary.total_strokes,
        distance_per_stroke=interval_summary.distance_per_stroke,
        distance_per_stroke_imp=interval_summary.distance_per_stroke_imp,
        avg_heart_rate=interval_summary.avg_heart_rate,
        avg_cal_per_hour=interval_summary.avg_cal_per_hour,
        total_cals=interval_summary.total_cals,
        start_gps_lat=interval_summary.start_gps_lat,
        start_gps_lon=interval_summary.start_gps_lon,
    )

def build_per_stroke_data_db(per_stroke_data: PerStrokeData, interval_id: int) -> Collection[PerStrokeDataDb]:
    return [
        PerStrokeDataDb(
        interval_id=interval_id,
        interval=per_stroke_data.interval[stroke],
        distance=per_stroke_data.distance[stroke],
        distance_imp=per_stroke_data.distance_imp[stroke],
        elapsed_time=per_stroke_data.elapsed_time[stroke],
        split=per_stroke_data.split[stroke],
        speed=per_stroke_data.speed[stroke],
        split_imp=per_stroke_data.split_imp[stroke],
        speed_imp=per_stroke_data.speed_imp[stroke],
        stroke_rate=per_stroke_data.stroke_rate[stroke],
        strokes=per_stroke_data.strokes[stroke],
        distance_per_stroke=per_stroke_data.distance_per_stroke[stroke],
        distance_per_stroke_imp=per_stroke_data.distance_per_stroke_imp[stroke],
        heart_rate=per_stroke_data.heart_rate[stroke],
        cal_per_hour=per_stroke_data.cal_per_hour[stroke],
        total_cals=per_stroke_data.total_cals[stroke],
        gps_lat=per_stroke_data.gps_lat[stroke],
        gps_lon=per_stroke_data.gps_lon[stroke],
    ) for stroke in range(len(per_stroke_data.strokes))
    ]


def persist_speed_data(db_session: Session, speed_data: SpeedData) -> bool:
    session_summary_db = build_session_summary_db(speed_data.session_summary)
    db_session.add(session_summary_db)
    db_session.commit()

    interval_summary_db = build_interval_summary_db(speed_data.interval_summary, session_summary_db.id)
    db_session.add(interval_summary_db)
    db_session.commit()

    per_stroke_data_db = build_per_stroke_data_db(speed_data.per_stroke_data, interval_summary_db.id)
    db_session.add_all(per_stroke_data_db)
    db_session.commit()
    return True
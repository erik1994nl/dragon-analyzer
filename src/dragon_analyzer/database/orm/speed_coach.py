from datetime import timedelta
from sqlalchemy import ARRAY, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from dragon_analyzer.database.orm.db import Base

class SessionSummaryDb(Base):
    __tablename__ = "session_summary"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    intervals: Mapped[int]
    distance: Mapped[float]
    distance_imp: Mapped[float]
    total_elapsed_time: Mapped[timedelta]
    avg_split: Mapped[timedelta]
    avg_speed: Mapped[float]
    avg_split_imp: Mapped[timedelta]
    avg_speed_imp: Mapped[float]
    avg_stroke_rate: Mapped[float]
    total_strokes: Mapped[int]
    distance_per_stroke: Mapped[float]
    distance_per_stroke_imp: Mapped[float]
    avg_heart_rate: Mapped[str] = mapped_column(String(64))
    avg_cal_per_hr: Mapped[int]
    total_cals: Mapped[int]
    start_gps_lat: Mapped[float]
    start_gps_lon: Mapped[float]

class IntervalSummaryDb(Base):
    __tablename__ = "interval_summary"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    session_id: Mapped[int] = mapped_column(ForeignKey(SessionSummaryDb.id))
    interval: Mapped[int]
    total_distance: Mapped[float]
    total_distance_imp: Mapped[float]
    total_elapsed_time: Mapped[timedelta]
    avg_split: Mapped[timedelta]
    avg_speed: Mapped[float]
    avg_split_imp: Mapped[timedelta]
    avg_speed_imp: Mapped[float]
    avg_stroke: Mapped[float]
    total_strokes: Mapped[int]
    distance_per_stroke: Mapped[float]
    distance_per_stroke_imp: Mapped[float]
    avg_heart_rate: Mapped[str] = mapped_column(String(64))
    avg_cal_per_hour: Mapped[int]
    total_cals: Mapped[int]
    start_gps_lat: Mapped[float]
    start_gps_lon: Mapped[float]

class PerStrokeDataDb(Base):
    __tablename__ = "per_stroke_data"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    interval_id: Mapped[int] = mapped_column(ForeignKey(IntervalSummaryDb.id))
    interval: Mapped[int]
    distance: Mapped[float]
    distance_imp: Mapped[float]
    elapsed_time: Mapped[timedelta]
    split: Mapped[timedelta]
    speed: Mapped[float]
    split_imp: Mapped[timedelta]
    speed_imp: Mapped[float]
    stroke_rate: Mapped[float]
    strokes: Mapped[int]
    distance_per_stroke: Mapped[float]
    distance_per_stroke_imp: Mapped[float]
    heart_rate: Mapped[str] = mapped_column(String(64))
    cal_per_hour: Mapped[int]
    total_cals: Mapped[int]
    gps_lat: Mapped[float]
    gps_lon: Mapped[float]

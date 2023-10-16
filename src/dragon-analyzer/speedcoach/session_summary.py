from collections.abc import Mapping
import csv
from dataclasses import dataclass
from datetime import datetime, timedelta
from io import StringIO, TextIOWrapper

import pandas as pd

from utils import to_timedelta


@dataclass
class SessionSummary:
    intervals: int
    distance: float
    distance_imp: float
    total_elapsed_time: timedelta
    avg_split: timedelta
    avg_speed: float
    avg_split_imp: timedelta
    avg_speed_imp: float
    avg_stroke_rate: float
    total_strokes: int
    distance_per_stroke: float
    distance_per_stroke_imp: float
    avg_heart_rate: str
    avg_cal_per_hr: int
    total_cals: int
    start_gps_lat: float
    start_gps_lon: float

    @staticmethod
    def from_data(d: Mapping[str, str]) -> "SessionSummary":
        total_elapsed_time_t = datetime.strptime(d["total_elapsed_time"], "%H:%M:%S.%f")
        avg_split_t = datetime.strptime(d["avg_split"], "%H:%M:%S.%f")
        avg_split_imp_t = datetime.strptime(d["avg_split_imp"], "%H:%M:%S.%f")

        return SessionSummary(
            intervals=int(d["intervals"]),
            distance=float(d["distance"]),
            distance_imp=float(d["distance_imp"]),
            total_elapsed_time=to_timedelta(total_elapsed_time_t),
            avg_split=to_timedelta(avg_split_t),
            avg_speed=float(d["avg_speed"]),
            avg_split_imp=to_timedelta(avg_split_imp_t),
            avg_speed_imp=float(d["avg_speed_imp"]),
            avg_stroke_rate=float(d["avg_stroke_rate"]),
            total_strokes=int(d["total_strokes"]),
            distance_per_stroke=float(d["distance_per_stroke"]),
            distance_per_stroke_imp=float(d["distance_per_stroke_imp"]),
            avg_heart_rate=str(d["avg_heart_rate"]),
            avg_cal_per_hr=int(d["avg_cal_per_hr"]),
            total_cals=int(d["total_cals"]),
            start_gps_lat=float(d["start_gps_lat"]),
            start_gps_lon=float(d["start_gps_lon"]),
        )


SESSION_SUMMARY_FIELDNAMES = list(SessionSummary.__dataclass_fields__.keys())


def parse_session_summary(speed_file: TextIOWrapper):
    for _ in range(3):
        speed_file.readline()

    speed_dict_reader = csv.DictReader(
        speed_file, fieldnames=SESSION_SUMMARY_FIELDNAMES
    )
    return next(speed_dict_reader)


def parse_session_summary_df(speed_data: list[str], start: int, end: int):
    content = "\n".join(speed_data[start:end])
    return pd.read_csv(StringIO(content), header=None, names=SESSION_SUMMARY_FIELDNAMES)

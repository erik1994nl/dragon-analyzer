from collections import defaultdict
import csv
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections.abc import Mapping
from io import StringIO, TextIOWrapper

import pandas as pd

from utils import to_timedelta


@dataclass
class PerStrokeData:
    interval: list[int]
    distance: list[float]
    distance_imp: list[float]
    elapsed_time: list[timedelta]
    split: list[timedelta]
    speed: list[float]
    split_imp: list[timedelta]
    speed_imp: list[float]
    stroke_rate: list[float]
    strokes: list[int]
    distance_per_stroke: list[float]
    distance_per_stroke_imp: list[float]
    heart_rate: list[str]
    cal_per_hour: list[int]
    total_cals: list[int]
    gps_lat: list[float]
    gps_lon: list[float]

    @staticmethod
    def from_data(d: Mapping[str, str]) -> "PerStrokeData":
        elapsed_time_t = [
            datetime.strptime(elapsed_time, "%H:%M:%S.%f")
            for elapsed_time in d["elapsed_time"]
        ]
        split_t = [datetime.strptime(split, "%H:%M:%S.%f") for split in d["split"]]
        split_imp_t = [
            datetime.strptime(split_imp, "%H:%M:%S.%f") for split_imp in d["split_imp"]
        ]

        return PerStrokeData(
            interval=[int(interval) for interval in d["interval"]],
            distance=[float(distance) for distance in d["distance"]],
            distance_imp=[float(distance_imp) for distance_imp in d["distance_imp"]],
            elapsed_time=[
                to_timedelta(elapsed_time) for elapsed_time in elapsed_time_t
            ],
            split=[to_timedelta(split) for split in split_t],
            speed=[float(speed) for speed in d["speed"]],
            split_imp=[to_timedelta(split_imp) for split_imp in split_imp_t],
            speed_imp=[float(speed_imp) for speed_imp in d["speed_imp"]],
            stroke_rate=[float(stroke_rate) for stroke_rate in d["stroke_rate"]],
            strokes=[int(strokes) for strokes in d["strokes"]],
            distance_per_stroke=[
                float(distance_per_stroke)
                for distance_per_stroke in d["distance_per_stroke"]
            ],
            distance_per_stroke_imp=[
                float(distance_per_stroke_imp)
                for distance_per_stroke_imp in d["distance_per_stroke_imp"]
            ],
            heart_rate=[str(heart_rate) for heart_rate in d["heart_rate"]],
            cal_per_hour=[int(cal_per_hour) for cal_per_hour in d["cal_per_hour"]],
            total_cals=[int(total_cals) for total_cals in d["total_cals"]],
            gps_lat=[float(gps_lat) for gps_lat in d["gps_lat"]],
            gps_lon=[float(gps_lon) for gps_lon in d["gps_lon"]],
        )


PER_STROKE_DATA_FIELDNAMES = list(PerStrokeData.__dataclass_fields__.keys())


def parse_per_stroke_data(speed_file: TextIOWrapper) -> Mapping[str, str]:
    for _ in range(3):
        speed_file.readline()

    per_stroke_data_dict = defaultdict(list)
    speed_dict_reader = csv.DictReader(
        speed_file, fieldnames=PER_STROKE_DATA_FIELDNAMES
    )
    for speed_row in speed_dict_reader:
        for speed_row_key, speed_row_value in speed_row.items():
            per_stroke_data_dict[speed_row_key].append(speed_row_value)
    return dict(per_stroke_data_dict)


def parse_per_stroke_data_df(speed_data: list[str], start: int, end: int):
    content = "\n".join(speed_data[start:end])
    return pd.read_csv(StringIO(content), header=None, names=PER_STROKE_DATA_FIELDNAMES)

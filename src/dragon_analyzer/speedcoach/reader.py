from dataclasses import dataclass

import pandas as pd
from dragon_analyzer.speedcoach.interval_summary import (
    IntervalSummary,
    parse_interval_summary,
    parse_interval_summary_df,
)
from dragon_analyzer.speedcoach.per_stroke_data import (
    PerStrokeData,
    parse_per_stroke_data,
    parse_per_stroke_data_df,
)

from dragon_analyzer.speedcoach.session_summary import (
    SessionSummary,
    parse_session_summary,
    parse_session_summary_df,
)


SPEED_DATA_PATH = "./src/data/Speedcoach_Arjo_20231008_1118.csv"


@dataclass
class SpeedData:
    session_summary: SessionSummary
    interval_summary: IntervalSummary
    per_stroke_data: PerStrokeData


def read_data() -> SpeedData:
    "Read Speedcoach data"
    with open(SPEED_DATA_PATH) as speed_file:
        while True:
            speed_row_peek = speed_file.readline()
            if "Session Summary:" in speed_row_peek:
                session_summary = parse_session_summary(speed_file)
            elif "Interval Summaries:" in speed_row_peek:
                interval_summary = parse_interval_summary(speed_file)
            elif "Per-Stroke Data:" in speed_row_peek:
                per_stroke_data = parse_per_stroke_data(speed_file)
                break

        return SpeedData(
            session_summary=SessionSummary.from_data(session_summary),
            interval_summary=IntervalSummary.from_data(interval_summary),
            per_stroke_data=PerStrokeData.from_data(per_stroke_data),
        )


@dataclass
class SpeedDataDataFrame:
    session_summary: pd.DataFrame()
    interval_summary: pd.DataFrame()
    per_stroke_data: pd.DataFrame()


def read_data_data_frame() -> SpeedDataDataFrame:
    """Read Speedcoach data in Pandas DataFrame format"""
    with open(SPEED_DATA_PATH) as speed_file:
        speed_data = speed_file.readlines()
        data_index = data_sections(speed_data)

        return SpeedDataDataFrame(
            session_summary=parse_session_summary_df(
                speed_data,
                data_index.session_summary[0],
                data_index.session_summary[1],
            ),
            interval_summary=parse_interval_summary_df(
                speed_data,
                data_index.interval_summary[0],
                data_index.interval_summary[1],
            ),
            per_stroke_data=parse_per_stroke_data_df(
                speed_data,
                data_index.per_stroke_data[0],
                data_index.per_stroke_data[1],
            ),
        )


@dataclass
class DataIndex:
    session_summary: tuple[int, int]
    interval_summary: tuple[int, int]
    per_stroke_data: tuple[int, int]


def data_sections(d: list[str]) -> DataIndex:
    session_summary_start = d.index("Session Summary:\n")
    interval_summary_start = d.index("Interval Summaries:\n")
    per_stroke_data_start = d.index("Per-Stroke Data:\n")
    return DataIndex(
        session_summary=(session_summary_start + 4, interval_summary_start - 2),
        interval_summary=(interval_summary_start + 4, per_stroke_data_start - 3),
        per_stroke_data=(per_stroke_data_start + 4, len(d) - 1),
    )

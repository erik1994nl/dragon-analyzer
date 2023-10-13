from dataclasses import dataclass
import pandas as pd
from io import StringIO

SPEED_DATA_PATH = "./src/data/Speedcoach_Arjo_20231008_1118.csv"


@dataclass
class SpeedCoachLayout:
    header: int
    units: int
    content: tuple[int, int]


@dataclass
class DataIndex:
    session_summary: SpeedCoachLayout
    interval_summaries: SpeedCoachLayout
    per_stroke_data: SpeedCoachLayout


@dataclass
class SpeedData:
    session_summary: pd.DataFrame
    interval_summaries: pd.DataFrame
    per_stroke_data: pd.DataFrame


def read_data() -> SpeedData:
    with open(SPEED_DATA_PATH) as speed_file:
        speed_data = speed_file.readlines()
        data_index = data_sections(speed_data)

        return SpeedData(
            session_summary=parse_section_data(speed_data, data_index.session_summary),
            interval_summaries=parse_section_data(
                speed_data, data_index.interval_summaries
            ),
            per_stroke_data=parse_section_data(speed_data, data_index.per_stroke_data),
        )


def data_sections(d: list[str]) -> DataIndex:
    session_summary_start = d.index("Session Summary:\n")
    interval_summaries_start = d.index("Interval Summaries:\n")
    per_stroke_data_start = d.index("Per-Stroke Data:\n")
    return DataIndex(
        session_summary=SpeedCoachLayout(
            header=session_summary_start + 2,
            units=session_summary_start + 3,
            content=(session_summary_start + 4, interval_summaries_start - 2),
        ),
        interval_summaries=SpeedCoachLayout(
            header=interval_summaries_start + 2,
            units=interval_summaries_start + 3,
            content=(interval_summaries_start + 4, per_stroke_data_start - 3),
        ),
        per_stroke_data=SpeedCoachLayout(
            header=per_stroke_data_start + 2,
            units=per_stroke_data_start + 3,
            content=(per_stroke_data_start + 4, len(d) - 1),
        ),
    )


def parse_section_data(data: list[str], layout: SpeedCoachLayout) -> pd.DataFrame:
    header = data[layout.header]
    content = "\n".join(data[layout.content[0] : layout.content[1]])

    return pd.read_csv(StringIO(content), header=None, names=header.split(","))

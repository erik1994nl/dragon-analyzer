from datetime import datetime, timedelta

GORINCHEM_BACKGROUND = "./src/data/Gorinchem_dof.png"
GORINCHEM_LEFT = 4.9757476251584585
GORINCHEM_RIGHT = 4.990524247467946
GORINCHEM_BOTTOM = 51.8344074244189
GORINCHEM_TOP = 51.841285066146426


def to_timedelta(d: datetime) -> timedelta:
    return timedelta(
        hours=d.hour, minutes=d.minute, seconds=d.second, microseconds=d.microsecond
    )

from dataclasses import dataclass
from typing import TypedDict


@dataclass
class Schedule(TypedDict):
    Monday: int
    Tuesday: int
    Wednesday: int
    Thursday: int
    Friday: int
    Saturday: int
    Sunday: int


lauri_schedule: Schedule = {
    "Monday": 3,
    "Tuesday": 3,
    "Wednesday": 2,
    "Thursday": 2,
    "Friday": 2,
    "Saturday": 3,
    "Sunday": 0,
}

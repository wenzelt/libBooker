from dataclasses import dataclass


@dataclass
class MoodleCourse:
    title: str
    href: str


@dataclass
class DocInfo:
    title: str
    href: str
    extension: str

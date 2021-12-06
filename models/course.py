from dataclasses import dataclass


@dataclass
class MoodleCourse:
    title: str
    href: str


@dataclass
class FileInfo:
    title: str
    href: str

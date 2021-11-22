from enum import auto


class PageStatus:
    LOGIN = auto()
    RESERVATION_PAGE = auto()
    NON_BOOKABLE = auto()
    UNDEFINED = auto()


class SlotStatus:
    EARLY = "0"
    NOON = "1"
    LATE = "2"

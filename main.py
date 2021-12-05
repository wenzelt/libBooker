from parsers.booker_TUM import TUMBooker
from parsers.booker_LMU import LMUBooker

if __name__ == "__main__":
    asd = TUMBooker(
        name="Tom Wenzel",
        e_mail="tom.wenzel@tum.de",
        identifier="ga58goq",
        arguments={"location": "Garching"},
    )
    asd.book_room()
    asd = LMUBooker(
        name="Tom Wenzel",
        e_mail="tom.wenzel@tum.de",
        identifier="ga58goq",
        arguments={"location": "Garching"},
    )
    asd.book_room()

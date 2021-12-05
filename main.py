import asyncio

from parsers.booker_LMU import LMUBooker
from parsers.booker_TUM import TUMBooker


async def main():
    qwe = TUMBooker(
        name="Tom Wenzel",
        e_mail="tom.wenzel@tum.de",
        identifier="ga58goq",
        arguments={"location": "Garching"},
    )
    asd = LMUBooker(
        name="Laura Loew",
        e_mail="tom.wenzel@tum.de",
        identifier="ga58goq",
        arguments={"location": "Garching"},
    )
    # Schedule three calls *concurrently*:
    L = await asyncio.gather(qwe.book_room(), asd.book_room())
    print(L)


if __name__ == "__main__":
    asyncio.run(main())

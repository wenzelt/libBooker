import asyncio

from parsers.booker_LMU import LMUBooker
from parsers.booker_TUM import TUMBooker


async def main():
    tum = TUMBooker(
        name="Tom Wenzel",
        e_mail="tom.wenzel@tum.de",
        identifier="ga58goq",
        arguments={"location": "Garching"},
    )
    lmu = LMUBooker(
        name="Laura Loew",
        e_mail="tom.wenzel@tum.de",
        identifier="ga58goq",
        arguments={"location": "Philologikum"},
    )

    tasks = await asyncio.gather(tum.book_room("Garching"), lmu.book_room())
    print(tasks)


if __name__ == "__main__":
    asyncio.run(main())

import asyncio

from bookers.booker_LMU import LMUBooker
from bookers.booker_TUM import TUMBooker


async def main():
    # tum = TUMBooker(
    #     name="Tom Wenzel",
    #     e_mail="tom.wenzel@tum.de",
    #     identifier="ga58goq",
    #     arguments={"location": "Garching"},
    # )
    lmu = LMUBooker(
        name="Laura Loew",
        e_mail="tom.wenzel@tum.de",
        identifier="ga58goq",
        arguments={"location": "Philologikum"},
    )
    await asyncio.gather(lmu.book_room())


if __name__ == "__main__":
    asyncio.run(main())

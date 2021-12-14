import asyncio

import config
from scrapers.scrape_moodle import ScraperMoodle


async def main():
    tum = ScraperMoodle(
        arguments={
            "username": f"{config.USERNAME_MOODLE}",
            "password": f"{config.PW_MOODLE}",
        }
    )
    tasks = await asyncio.gather(tum.scrape())
    print(tasks)


if __name__ == "__main__":
    asyncio.run(main())

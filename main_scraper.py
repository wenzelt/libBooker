import asyncio

from scrapers.scrape_moodle import ScraperMoodle


async def main():
    tum = ScraperMoodle(arguments={"username": "ga58goq", "password": "Supert0ast96"})
    tasks = await asyncio.gather(tum.scrape())
    print(tasks)


if __name__ == "__main__":
    asyncio.run(main())

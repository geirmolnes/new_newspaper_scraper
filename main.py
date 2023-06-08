from dotenv import load_dotenv
from Scraper import Scraper
import db  # You can now directly import the db module
import time
from logging_config import configure_logger

logger = configure_logger(__name__)

# Load environment variables
load_dotenv("/home/geirmol/new_archiver/.env")


def main():
    """
    Scrape the articles, store them in a CSV,
    and then insert the articles into the database.
    """

    start_time = time.time()

    scraper = Scraper("/home/geirmol/new_archiver/newspapers.json")
    articles = scraper.scrape()
    scraper.create_csv(articles)

    db.insert_articles(articles)  # You can directly call db functions

    end_time = time.time()  # Record the end time
    elapsed_time_seconds = (
        end_time - start_time
    )  # Calculate the elapsed time in seconds
    elapsed_time_minutes = elapsed_time_seconds // 60  # Get the elapsed minutes
    elapsed_time_seconds %= (
        60  # Get the remaining seconds after the minutes are subtracted
    )

    logger.info(
        f"\n##\nTime taken: {elapsed_time_minutes} minutes {elapsed_time_seconds} seconds.\n##\n"
    )


if __name__ == "__main__":
    main()

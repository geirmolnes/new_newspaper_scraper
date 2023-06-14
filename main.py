from Scraper import Scraper
import db  # You can now directly import the db module
import time
from logging_config import configure_logger
from config import CSV_PATH, DB_STRING, NEWSPAPERS_JSON_PATH, LOGGER_PATH

logger = configure_logger(__name__, log_path=LOGGER_PATH)


def main():
    """
    Scrape the articles, store them in a CSV,
    insert the articles into the database.
    """

    start_time = time.time()
    db.create_table(db_string=DB_STRING, table_name="newspapers8")

    scraper = Scraper(NEWSPAPERS_JSON_PATH)
    articles = scraper.scrape()
    scraper.create_csv(articles, csv_path=CSV_PATH)

    db.insert_articles(articles, db_string=DB_STRING)

    end_time = time.time()
    elapsed_time_seconds = end_time - start_time
    elapsed_time_minutes = elapsed_time_seconds // 60
    elapsed_time_seconds %= 60

    logger.info(
        f"\n##\nTime taken: {elapsed_time_minutes} minutes {elapsed_time_seconds} seconds.\n##\n",
    )


if __name__ == "__main__":
    main()

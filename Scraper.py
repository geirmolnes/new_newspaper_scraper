import json
import feedparser
import newspaper
import pandas as pd
from datetime import datetime
from time import strftime
import random
from logging_config import configure_logger
from UrlExtractor import get_canonical_url
import db


logger = configure_logger(__name__)


class Scraper:
    """
    Scraper class to scrape articles from the provided newspapers.
    """

    def __init__(self, newspapers_json, max_articles_per_newspaper=15):
        """
        Initialize the Scraper with a json file of newspapers.

        :param newspapers_json: JSON file with newspaper info.
        :param max_articles_per_newspaper: Maximum number of articles to be scraped from each newspaper.
        """
        self.newspapers = self._load_newspapers(newspapers_json)
        self.max_articles_per_newspaper = max_articles_per_newspaper
        self.all_feed_data = self._fetch_feed_data()

    def scrape(self):
        """
        Scrape the articles from the feed data.

        :return: List of scraped article data.
        """
        articles = []
        for entry in self._shuffled_feed_data():
            article = self._scrape_article(entry)
            if article is not None:
                articles.append(article)
        return articles

    def _load_newspapers(self, newspapers_json):
        """
        Load newspapers from a JSON file.
        """
        with open(newspapers_json, "r") as file:
            data = json.load(file)
            return data["newspapers"]

    def _fetch_feed_data(self):
        """
        Fetch feed data for all provided newspapers.
        """
        feed_data = []
        total_urls = 0
        new_urls = 0
        for paper in self.newspapers:
            try:
                feed = feedparser.parse(paper["feed_url"])
                for entry in feed.entries[: self.max_articles_per_newspaper]:
                    total_urls += 1
                    if not db.url_in_db(None, entry.link):
                        entry["newspaper"] = paper
                        feed_data.append(entry)
                        new_urls += 1
            except Exception as e:
                logger.error(
                    f"Error fetching feed data from {paper['newspaper_name']}\n{e}\n"
                )
        logger.info(f"Total URLs fetched: {total_urls}. New URLs: {new_urls}.")
        return feed_data

    def _shuffled_feed_data(self):
        """
        Returns a shuffled version of the feed data
        """
        feed_data = self.all_feed_data.copy()
        random.shuffle(feed_data)
        return feed_data

    @staticmethod
    def _get_article_content(url):
        """
        Download and parse an article from a given URL using newspaper3k.

        :param url: URL of the article to parse.
        :return: Parsed Article object or None if an error occurs.
        """
        try:
            article = newspaper.Article(url)
            article.download()
            article.parse()
        except Exception as e:
            logger.error(f"Error downloading article at {url}\n{e}\n")
            return None
        return article

    @staticmethod
    def _get_published_time(article, entry):
        """
        Get the published time of the article if available.

        :param article: Parsed Article object.
        :param entry: Feed entry object.
        :return: Published time as a string or None if not available.
        """
        if article.publish_date:
            return article.publish_date.strftime("%Y-%m-%d %H:%M")
        elif hasattr(entry, "published_parsed"):
            return strftime("%Y-%m-%d %H:%M", entry.published_parsed)
        return None

    def _scrape_article(self, entry):  # sourcery skip: use-named-expression
        """
        Scrape data from a given article.

        :param entry: Feed entry object containing article information.
        :return: Dictionary with scraped article data, or None if an error occurs.
        """
        paper = entry["newspaper"]
        article = self._get_article_content(entry.link)
        if not article:
            return None

        canonical_url = get_canonical_url(paper["newspaper_name"], entry.link)
        published_time = self._get_published_time(article, entry)

        data = {
            "published_time": published_time,
            "newspaper": paper.get("newspaper_name"),
            "headline": entry.title,
            "canonical_url": canonical_url,
            "non_canonical_url": entry.link,
            "article_text": article.text,
            "media_type": paper.get("media_type"),
            "fetched_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }

        missing_fields = [field for field, value in data.items() if not value]

        if missing_fields:
            logger.warning(
                f"Data not found for fields {missing_fields} for article at {entry.link}"
            )

        return data

    @staticmethod
    def create_csv(data):
        """
        Create a CSV file with the scraped data.
        """
        df = pd.DataFrame(data)
        df.to_csv(
            "/home/geirmol/new_archiver/data.csv", index=False
        )  # Use absolute path here

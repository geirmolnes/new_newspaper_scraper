import psycopg2
from config import DB_STRING


def url_in_db(canonical_url, non_canonical_url, db_string=DB_STRING):
    with psycopg2.connect(db_string) as conn, conn.cursor() as cur:
        select_query = "SELECT 1 FROM newspapers8 WHERE canonical_url = %s OR non_canonical_url = %s"
        cur.execute(select_query, (canonical_url, non_canonical_url))
        return cur.fetchone() is not None


def insert_articles(articles, db_string=DB_STRING):
    with psycopg2.connect(db_string) as conn, conn.cursor() as cur:
        for article in articles:
            canonical_url = article.get("canonical_url")
            non_canonical_url = article.get("non_canonical_url")

            if not url_in_db(canonical_url, non_canonical_url):
                values = [
                    article.get("published_time"),
                    article.get("newspaper"),
                    article.get("headline"),
                    canonical_url,
                    non_canonical_url,
                    article.get("article_text"),
                    article.get("media_type"),
                    article.get("fetched_time"),
                ]
                insert = """
                INSERT INTO newspapers8
                (published_time, newspaper, headline, canonical_url, non_canonical_url,
                article_text, media_type, fetched_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                try:
                    cur.execute(insert, values)
                    conn.commit()
                except Exception as e:
                    print(f"An error occurred: {e}")
                    conn.rollback()

# News Archiver

This project is a Python-based scraper that pulls in articles from various news outlets, stores the data in a CSV file, and inserts the articles into a database.

## Setup

### Prerequisites

- Python 3.7 or higher
- PostgreSQL Database

### Installation

1. Clone the repository to your local machine.
    ```
    git clone https://github.com/geirmol/new_newspaper_scraper.git
    ```

2. Navigate to the project directory.
    ```
    cd new_newspaper_scraper
    ```

3. Install the necessary Python packages.
    ```
    pip install -r requirements.txt
    ```

4. Set up the PostgreSQL database. You will need to provide a connection string in the `db.py` module.

## Usage

After setting up the project, you can run the program with: python main.py

## Features

- Scraper: The `Scraper` class is the heart of this project. It reads a JSON file containing a list of newspapers to scrape. For each newspaper, it downloads the RSS feed, parses the articles, and stores the resulting data.

- Database: This script interacts with a PostgreSQL database to store article data. It checks whether a non-canonical URL is already in the database before starting the scraping process, preventing duplicate work.

- Logging: The program includes a custom logging configuration. This can be easily adapted to change the level of logging detail, add new handlers, or otherwise modify how logging is handled.

## Project Structure

- `main.py`: The main script to run the project.
- `Scraper.py`: The script containing the `Scraper` class, which is responsible for scraping the articles.
- `db.py`: The script containing the `Database` class, which interacts with a PostgreSQL database to store article data.
- `logging_config.py`: The script which sets up custom logging for the project.
- `UrlExtractor.py`: A helper script for dealing with URLs in the articles.
- `newspapers.json`: A JSON file containing the list of newspapers to scrape.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](#) if you want to contribute.

## License

Distributed under the MIT License. See `LICENSE` for more information. 

## Contact

Geir Molnes - g.molnes@gmail.com

Project Link: https://github.com/geirmolnes/new_newspaper_scraper

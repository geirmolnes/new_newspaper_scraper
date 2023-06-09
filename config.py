import os
from dotenv import load_dotenv

# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the .env file path
env_file = os.path.join(current_dir, ".env")

# Load the .env file
load_dotenv(env_file)

# Now load the environment variables
DB_STRING = os.getenv("DB_STRING")

# Construct the paths for the CSV, LOGGER, and NEWSPAPER files
CSV_PATH = os.path.join(current_dir, os.getenv("CSV_FILE"))
LOGGER_PATH = os.path.join(current_dir, os.getenv("LOGGER_FILE"))
NEWSPAPERS_JSON_PATH = os.path.join(current_dir, os.getenv("NEWSPAPERS_JSON_FILE"))

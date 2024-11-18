# Set base URL, API parameters, and file path for saving data
# import os

# os.makedirs(OUTPUT_DIR, exist_ok=True)
# os.makedirs(PROCESSED_DIR, exist_ok=True)

BASE_URL = "http://export.arxiv.org/api/query"
OUTPUT_DIR = "./arxiv_data/raw_data/"
PROCESSED_DIR = "../data"
FINAL_DATA_PATH = "./data/arxiv_data.csv"

# API rate limit: 3 requests per second
RATE_LIMIT = 3
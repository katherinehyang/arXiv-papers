import pyalex
import time
import csv

from pyalex import Works, Authors, Sources, Institutions, Topics, Publishers, Funders
from pyalex import config

pyalex.config.email = "ky107@wellesley.edu"

config.max_retries = 3
config.retry_backoff_factor = 0.5
config.retry_http_codes = [429, 500, 503]

def get_works():
    Works().search("artificial intelligence").get()

# Constants
MAX_PAPERS = 100000
RESULTS_PER_PAGE = 100
REQUESTS_PER_SECOND = 10
CSV_FILE = "ai_100k_papers.csv"

# Save to CSV
def save_to_csv(papers, filename, append=False):
    mode = "a" if append else "w"
    with open(filename, mode, newline="", encoding="utf-8") as csvfile:
        fieldnames = ["id", "title", "doi", "publication_date", "abstract"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header only if not appending
        if not append:
            writer.writeheader()

        for paper in papers:
            writer.writerow({
                "id": paper.get("id", "N/A"),
                "title": paper.get("title", "N/A"),
                "doi": paper.get("doi", "N/A"),
                "publication_date": paper.get("publication_date", "N/A"),
                "abstract": paper.get("abstract", "N/A")
            })

# Fetch Papers
def fetch_openalex_papers(search_query):
    all_papers = []
    total_fetched = 0
    page_number = 1

    # Get total results count
    total_results = Works.filter(search=search_query).count()
    print(f"Total papers available: {total_results}")

    while total_fetched < min(total_results, MAX_PAPERS):
        try:
            print(f"Fetching page {page_number}...")
            page = Works.filter(search=search_query).paginate(per_page=RESULTS_PER_PAGE, page=page_number)
            
            if not page or len(page) == 0:  # Break if no results
                print(f"No results on page {page_number}. Exiting.")
                break

            all_papers.extend(page)
            total_fetched += len(page)

            # Save incrementally
            save_to_csv(page, CSV_FILE, append=True)
            print(f"Fetched {len(page)} results. Total fetched: {total_fetched}/{MAX_PAPERS}.")

            page_number += 1

            # Respect rate limit
            time.sleep(0.1)  # Spread requests to avoid hitting the limit

        except Exception as e:
            print(f"Error fetching page {page_number}: {e}. Skipping.")
            page_number += 1
            continue

    return all_papers



# Main
def main():
    search_query = "Artificial Intelligence"
    print("hi")

    # Fetch data from OpenAlex API
    print(f"Starting OpenAlex query for: {search_query}")
    fetch_openalex_papers(search_query)

    print(f"Papers saved to {CSV_FILE}")

if __name__ == "__main__":
    main()

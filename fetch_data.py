# arXiv query API

from datetime import datetime, timedelta

import requests
import time
import config

def fetch_arxiv_data(query, start, max_results):
    """
    Fetch data through range of papers.
    """
    url = f"{config.BASE_URL}?search_query={query}&start={start}&max_results={max_results}"

    try:
        response = requests.get(url)
        time.sleep(3)  # arXiv API rate limit - 3 seconds
        
        if response.status_code == 200:
            print(f"Fetching results from {start} to {start + max_results}")
            return response.content
        else:
            print(f"Error fetching data: {response.status_code}")
            return None
        
    except requests.exceptions.RequestException as e:
        print(f"Error with the request: {e}")
        return None
    

def generate_date_ranges(start_date, end_date):
    """
    Generate date ranges with yearly intervals.
    """
    ranges = []
    current_start = start_date

    while current_start < end_date:
        # Calculate the end of the current year interval
        try:
            current_end = current_start.replace(year=current_start.year + 1)
        except ValueError:  # Handle non-leap years
            current_end = current_start + (datetime(current_start.year + 1, 1, 1) - datetime(current_start.year, 1, 1))

        if current_end > end_date:
            current_end = end_date

        ranges.append((current_start, current_end - timedelta(days=1)))
        current_start = current_end

    return ranges

def fetch_by_date_range(category, start_date, end_date):
    """
    Fetch papers by date range.
    """
    date_ranges = generate_date_ranges(datetime.strptime(start_date, "%Y-%m-%d"),
                                       datetime.strptime(end_date, "%Y-%m-%d"))

    for start, end in date_ranges:
        start_str = start.strftime("%Y-%m-%d")
        end_str = end.strftime("%Y-%m-%d")
        print(f"Fetching papers from {start_str} to {end_str}...")

        # Fetch papers for this range
        try:
            page = Works.filter(search=category,
                                from_publication_date=start_str,
                                to_publication_date=end_str).paginate(per_page=100)
            save_to_csv(page, CSV_FILE, append=True)
        except Exception as e:
            print(f"Error fetching papers for range {start_str} to {end_str}: {e}")
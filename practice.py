BASE_URL = "http://export.arxiv.org/api/query"

import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import requests
import time
import pandas as pd
import os

def generate_date_ranges(start_date, end_date):
    """
    Generate date ranges with yearly intervals.

    @param start_date: The start date of the date range
    @param end_date: The end date of the date range
    @return: A list of tuples, each containing the start and end dates of 
             a date range
    """
    ranges = []
    current_start = start_date

    while current_start < end_date:
        current_end = current_start.replace(year=current_start.year + 1)    
    
        if current_end > end_date:
            current_end = end_date

        ranges.append( (current_start, current_end) )
        current_start = current_end + timedelta(days=1)

    return ranges

def parse_arxiv_response(response_data):
    """
    Parse the XML data returned from the arXiv API and return a list of 
    dictionaries, each containing the title, authors, published date, abstract, 
    subjects, and citation of a paper.

    @param response_data: The XML data returned by the arXiv API
    @return: A list of dictionaries, each representing a paper
    """
    tree = ET.ElementTree(ET.fromstring(response_data))
    root = tree.getroot()

    entries = []
    
    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title = entry.find("{http://www.w3.org/2005/Atom}title").text if entry.find("{http://www.w3.org/2005/Atom}title") is not None else "Untitled"
        authors = [author.find("{http://www.w3.org/2005/Atom}name").text for author in entry.findall("{http://www.w3.org/2005/Atom}author")]
        published = entry.find("{http://www.w3.org/2005/Atom}published").text
        abstract = entry.find("{http://www.w3.org/2005/Atom}summary").text
        subjects = [category.attrib['term'] for category in entry.findall("{http://www.w3.org/2005/Atom}category")]
        citation = entry.find("{http://www.w3.org/2005/Atom}id").text

        entries.append({
            'title': title,
            'authors': authors,
            'published': published,
            'abstract': abstract,
            'subjects': ", ".join(subjects),
            'citation': citation
        })
    
    return entries


def process_data(parsed_data):
    """
    Process the parsed data and save it to a CSV file.

    @param parsed_data: List of dictionaries, each containing the title, authors, 
                        published date, abstract, subjects, and citation of a paper
    """
    df = pd.DataFrame(parsed_data)
    output_path = 'data/practice.csv'

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if os.path.exists(output_path):
        # If the file exists, append to it without rewriting headers
        df.to_csv(output_path, mode='a', index=False, header=False)
        print(f"Data appended to existing file: {output_path}")
    else:
        # If the file doesn't exist, create it and write the headers
        df.to_csv(output_path, mode='w', index=False)
        print(f"New file created and data written to: {output_path}")

def fetch_arxiv_data(url):
    """
    Fetch data from the given arXiv API URL.

    Sends a GET request to the specified URL and returns the content of the 
    response if successful. Handles request exceptions and prints error messages 
    for unsuccessful attempts.

    @param url: The URL to send the GET request to.
    @return: The content of the response if the request is successful, 
             otherwise None.
    """
    try:
        response = requests.get(url)
        time.sleep(3)  # arXiv API rate limit - 3 seconds
        
        if response.status_code == 200:
            print(f"Success")
            return response.content
        else:
            print(f"Error fetching data: {response.status_code}")
            return None
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def fetch_by_date_range(query, start_date, end_date, max_results):
    """
    Fetch papers from the arXiv API by date range.

    Generates date ranges between the given start and end dates, then iteratively 
    fetches papers from arXiv for each date range using paginated requests. 
    It processes and saves the fetched data.

    @param query: The search query for the arXiv API.
    @param start_date: The start date of the date range in "YYYY-MM-DD" format.
    @param end_date: The end date of the date range in "YYYY-MM-DD" format.
    @param max_results: The maximum number of results to fetch per request.
    """
    date_ranges = generate_date_ranges(datetime.strptime(start_date, "%Y-%m-%d"),
                                       datetime.strptime(end_date, "%Y-%m-%d"))

    for start, end in date_ranges:
        start_str = start.strftime("%Y-%m-%d")
        end_str = end.strftime("%Y-%m-%d")
        print(f"Fetching papers from {start_str} to {end_str}...")

        start_index = 0
        while True:
            url = (
                f"{BASE_URL}?search_query={query}&start_date={start_str}&end_date={end_str}"
                f"&start={start_index}&max_results={max_results}"
            )
            response = fetch_arxiv_data(url)
            if response is None:
                break  # Stop if an error occurs

            parsed_data = parse_arxiv_response(response)
            if not parsed_data:
                print("No more data to fetch.")
                break

            process_data(parsed_data)
            start_index += max_results




def main():
    query = 'cat:cs.AI'  # The search query for arXiv
    start_date = '2020-01-01'  # Start date for date range
    end_date = '2021-12-31'  # End date for date range
    max_results = 200  # Number of results to fetch per query

    print("Fetching data from arXiv...")
    fetch_by_date_range(query, start_date, end_date, max_results)

if __name__ == "__main__":
    main()
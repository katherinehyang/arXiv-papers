import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import time
import os
import pandas as pd



def fetch_arxiv_data(query, start, max_results):
    # Define the query parameters
    params = {
        "search_query": query,           # Query parameter
        "start": start,                     # Start index for results
        "max_results": max_results,         # Number of results to fetch
        "sortBy": "submittedDate",          # Sort by submission date
        # "sortOrder": "ascending"           # Sort order (descending)
    }

    query_url = f"{BASE_URL}?{urllib.parse.urlencode(params)}"
    print(f"Fetching results {start} to {start + max_results - 1}...")

    try:
        response = urllib.request.urlopen(query_url)
        time.sleep(3)  # arXiv API rate limit - 3 seconds

        if response.status == 200:
            print("Successfully fetched data!")
            return response.read()  # Return the response content as bytes
        else:
            print(f"Failed with status code: {response.status}")
            return None
    except urllib.error.URLError as e:
        print(f"Error fetching data: {e}")
        return None

def parse_arxiv_response(response_data):
    root = ET.fromstring(response_data)
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


def process_data(parsed_data, count):
    """
    Process the parsed data and save it to a CSV file.

    @param parsed_data: List of dictionaries, each containing the title, authors, 
                        published date, abstract, subjects, and citation of a paper
    """
    df = pd.DataFrame(parsed_data)
    output_path = f'data/practice_{count}.csv'

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if os.path.exists(output_path):
        # If the file exists, append to it without rewriting headers
        df.to_csv(output_path, mode='a', index=False, header=False)
        print(f"Data appended to existing file: {output_path}")
    else:
        # If the file doesn't exist, create it and write the headers
        df.to_csv(output_path, mode='w', index=False)
        print(f"New file created and data written to: {output_path}")




BASE_URL = "http://export.arxiv.org/api/query"
query = "cat:cs.AI"
max_results = 2000

def main():
    # Find total num of results in query
    url = f"{BASE_URL}?search_query={query}&max_results=0"
    response = urllib.request.urlopen(url)
    response_data = response.read()
    root = ET.fromstring(response_data)
    total_results = int(root.find("{http://a9.com/-/spec/opensearch/1.1/}totalResults").text)
    print(f"Total results for category cs.AI: {total_results}")

    count = 4
    start = 0
    stop = 20000

    while start < stop:        
        response_data = fetch_arxiv_data(query, start, max_results)

        if response_data:
            print("Parsing response data...")
            parsed_data = parse_arxiv_response(response_data)

            print("Processing and saving data...")
            process_data(parsed_data, count)

        start += max_results

    
    print("Reached 11000 results")

if __name__ == "__main__":
    main()
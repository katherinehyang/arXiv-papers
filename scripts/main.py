from fetch_data import fetch_arxiv_data
from parser import parse_arxiv_response
from processor import process_data

def main():
    query = 'machine learning'  # The search query for arXiv
    start = 0  # Start index for pagination
    max_results = 100  # Number of results to fetch per query

    # Fetch data from arXiv API
    print("Fetching data from arXiv...")
    response_data = fetch_arxiv_data(query, start, max_results)
    
    if response_data:
        # Parse the fetched data
        print("Parsing response data...")
        parsed_data = parse_arxiv_response(response_data)
        
        # Process and save the data
        print("Processing and saving data...")
        process_data(parsed_data)
        
    else:
        print("Failed to fetch or parse data.")

if __name__ == "__main__":
    main()
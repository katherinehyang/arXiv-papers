from fetch_data import fetch_arxiv_data
from parser import parse_arxiv_response
from processor import process_data
import xml.etree.ElementTree as ET

def main():
    query = 'cat:cs.AI'  # The search query for arXiv
    start = 0  # Start index for pagination
    max_results = 200  # Number of results to fetch per query

    # Fetch data from arXiv API
    print("Fetching data from arXiv...")
    response_data = fetch_arxiv_data(query, start, max_results)
    
    if response_data:
        # Parse the fetched data
        print("Parsing response data...")
        parsed_data = parse_arxiv_response(response_data)

        tree = ET.ElementTree(ET.fromstring(response_data))
        root = tree.getroot()

        total_results = int(root.find("{http://a9.com/-/spec/opensearch/1.1/}totalResults").text)
        print(f"Total results found: {total_results}")
        
        # Process and save the data
        print("Processing and saving data...")
        process_data(parsed_data)

        # Start a loop to fetch additional results if needed
        fetched_results = max_results  # We already fetched the first batch of results
    

        while fetched_results < total_results:
            start = fetched_results  # Update the 'start' for the next batch
            print(f"Fetching more data starting from result {start}...")
            response_data = fetch_arxiv_data(query, start, max_results)
            
            if response_data:
                # Parse and process the fetched data
                print("Parsing response data...")
                parsed_data = parse_arxiv_response(response_data)
                print("Processing and saving data...")
                process_data(parsed_data)
                
                # Update the count of fetched results
                fetched_results += max_results
                print(f"Fetched {fetched_results} results so far.")
                
            else:
                print("Error fetching more data.")
                break
    else:
        print("Failed to fetch or parse data.")

if __name__ == "__main__":
    main()
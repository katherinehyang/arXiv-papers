# fetch 

import requests
import time
import config

def fetch_arxiv_data(query, start=0, max_results=100):
    url = f"{config.BASE_URL}?search_query={query}&start={start}&max_results={max_results}"

    try:
        response = requests.get(url)
        time.sleep(3)  # arXiv API rate limit - 3 seconds
        
        if response.status_code == 200:
            return response.content
        else:
            print(f"Error fetching data: {response.status_code}")
            return None
        
    except requests.exceptions.RequestException as e:
        print(f"Error with the request: {e}")
        return None
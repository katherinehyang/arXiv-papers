# Clean data

import pandas as pd

def process_data(parsed_data):
    df = pd.DataFrame(parsed_data)
    
    # Example: Clean data, remove missing or irrelevant columns if necessary
    df.dropna(subset=['title'], inplace=True)  # Remove rows with missing titles
    
    # Save the cleaned data to a CSV file
    df.to_csv('../data/processed_data.csv', index=False)
    print("Data processed and saved to 'data/processed_data.csv'")
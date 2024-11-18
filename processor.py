# Clean data

import pandas as pd
import os
# import config

def process_data(parsed_data):
    df = pd.DataFrame(parsed_data)
    
    # Example: Clean data, remove missing or irrelevant columns if necessary
    if 'title' in df.columns:
        df.dropna(subset=['title'], inplace=True)  # Remove rows with missing titles
    else:
        print("No 'title' column in data.")

    
    # Save the cleaned data to a CSV file
    # output_file = f"{config.PROCESSED_DIR}/processed_data.csv"
    # df.to_csv(output_file, index=False)
    # print("Data processed and saved to 'data/processed_data.csv'")

    output_path = 'data/processed_data.csv'

    if os.path.exists(output_path):
        # If the file exists, append to it without rewriting headers
        df.to_csv(output_path, mode='a', index=False, header=False)
        print(f"Data appended to existing file: {output_path}")
    else:
        # If the file doesn't exist, create it and write the headers
        df.to_csv(output_path, mode='w', index=False)
        print(f"New file created and data written to: {output_path}")

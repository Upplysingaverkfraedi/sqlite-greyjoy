import os
import pandas as pd

# Paths to directories containing CSV files
results_dir = '/Users/haatlason/Documents/GitHub/sqlite-greyjoy/sql1/results'
metadata_dir = '/Users/haatlason/Documents/GitHub/sqlite-greyjoy/sql1/metadata'

# Paths to save merged files
merged_results_file = '/Users/haatlason/Documents/GitHub/sqlite-greyjoy/sql1/all_results.csv'
merged_metadata_file = '/Users/haatlason/Documents/GitHub/sqlite-greyjoy/sql1/all_metadata.csv'


def merge_csv_files(input_dir, output_file, expected_columns=None):
    """
    Merge all CSV files in the input directory into a single CSV file and save to output_file.
    :param input_dir: Directory containing CSV files to merge
    :param output_file: File path to save the merged CSV file
    :param expected_columns: Optional list of expected columns to ensure consistent structure
    """
    dfs = []

    # Iterate over all CSV files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.csv'):
            file_path = os.path.join(input_dir, filename)
            print(f"Merging {file_path}")

            # Load the CSV file
            df = pd.read_csv(file_path)

            # Check if expected columns are provided
            if expected_columns:
                # Filter columns that exist in the DataFrame and fill missing columns with NaN
                df = df.reindex(columns=expected_columns, fill_value='N/A')

            dfs.append(df)

    # Concatenate all DataFrames
    if dfs:
        merged_df = pd.concat(dfs, ignore_index=True)

        # Save the merged DataFrame to a new CSV file
        merged_df.to_csv(output_file, index=False)
        print(f"Merged file saved at: {output_file}")
    else:
        print("No CSV files found to merge.")


def main():
    # Expected columns for results and metadata CSVs
    expected_results_columns = ['id', 'hlaup_id', 'nafn', 'timi', 'kyn', 'aldur']
    expected_metadata_columns = ['id', 'upphaf', 'endir', 'nafn', 'fjoldi']

    # Merge all results CSV files
    print("Merging results CSV files...")
    merge_csv_files(results_dir, merged_results_file, expected_results_columns)

    # Merge all metadata CSV files
    print("Merging metadata CSV files...")
    merge_csv_files(metadata_dir, merged_metadata_file, expected_metadata_columns)


if __name__ == "__main__":
    main()

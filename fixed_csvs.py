import pandas as pd
import sqlite3

# File paths for the CSV files
results_file = '/Users/haatlason/Documents/GitHub/sqlite-greyjoy/sql1/all_results.csv'
metadata_file = '/Users/haatlason/Documents/GitHub/sqlite-greyjoy/sql1/all_metadata.csv'

# Database file path
db_file = '/Users/haatlason/Documents/GitHub/sqlite-greyjoy/sql1/timataka.db'

def load_and_clean_results_csv(file_path):
    df = pd.read_csv(file_path)
    print(f"Columns in {file_path}: {df.columns.tolist()}")
    df.rename(columns={
        'id': 'hlaup_id',     # Race ID
        'hlaup_id': 'rank',   # Participant's rank
        'Name': 'nafn',
        'Time': 'timi',
        'Year': 'aldur'
    }, inplace=True)
    expected_columns = ['rank', 'hlaup_id', 'nafn', 'timi', 'kyn', 'aldur']
    df = df[expected_columns]
    df['timi'] = df['timi'].fillna('00:00:00')
    df['nafn'] = df['nafn'].fillna('Unknown')
    return df

def load_and_clean_metadata_csv(file_path):
    df = pd.read_csv(file_path)
    expected_columns = ['id', 'upphaf', 'endir', 'nafn', 'fjoldi']
    df = df[expected_columns]
    return df

def check_for_duplicates(df, subset_columns):
    initial_count = len(df)
    duplicates = df[df.duplicated(subset=subset_columns, keep=False)]
    if not duplicates.empty:
        print(f"Duplicates found based on columns {subset_columns}:")
        print(duplicates.head(10))
        df = df.drop_duplicates(subset=subset_columns, keep='first')
        duplicates_removed = initial_count - len(df)
        print(f"Number of duplicates removed: {duplicates_removed}")
    else:
        print(f"No duplicates found based on columns {subset_columns}.")
    print(f"Number of rows after duplicate removal: {len(df)}")
    return df

def import_csv_to_sqlite(df, table_name, conn):
    if table_name == 'hlaup':
        df.to_sql(table_name, conn, if_exists='append', index=False)
    else:
        df.to_sql(table_name, conn, if_exists='append', index=False)

def main():
    # Load and clean the metadata (hlaup) CSV
    print("Loading and cleaning metadata CSV (hlaup)...")
    metadata_df = load_and_clean_metadata_csv(metadata_file)
    metadata_df['id'] = metadata_df['id'].astype(int)
    metadata_df = check_for_duplicates(metadata_df, subset_columns=['id'])
    print(f"Number of rows in metadata_df: {len(metadata_df)}")

    # Load and clean the results (timataka) CSV
    print("Loading and cleaning results CSV (timataka)...")
    results_df = load_and_clean_results_csv(results_file)
    results_df['rank'] = results_df['rank'].astype(int)
    results_df['hlaup_id'] = results_df['hlaup_id'].astype(int)
    results_df['nafn'] = results_df['nafn'].str.strip().str.lower()
    print(f"Number of rows in results_df after loading: {len(results_df)}")

    # Check for duplicates
    print("Checking for duplicates based on hlaup_id and nafn...")
    results_df = check_for_duplicates(results_df, subset_columns=['hlaup_id', 'nafn'])
    print(f"Number of rows in results_df after duplicate removal: {len(results_df)}")

    # Connect to SQLite database
    print("Connecting to SQLite database...")
    conn = sqlite3.connect(db_file)

    # Import data into SQLite
    print("Importing cleaned metadata into SQLite (hlaup)...")
    import_csv_to_sqlite(metadata_df, 'hlaup', conn)
    print("Importing cleaned results into SQLite (timataka)...")
    import_csv_to_sqlite(results_df, 'timataka', conn)

    conn.close()
    print("Data successfully imported into SQLite database.")

if __name__ == '__main__':
    main()

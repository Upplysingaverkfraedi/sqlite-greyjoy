import re
import requests
import pandas as pd
import argparse
import json
import os

# Fall til að lesa hlekki úr txt skránni
def read_links_from_file(file_path):
    with open(file_path, 'r') as file:
        links = [line.strip() for line in file if line.strip()]
    return links

# Regluleg segð til að finna dálkaheiti (thead)
def parse_column_headers(html):
    header_pattern = re.compile(r'<thead.*?>(.*?)</thead>', re.S)
    headers = header_pattern.search(html)
    if headers:
        header_row = headers.group(1)
        header_data_pattern = re.compile(r'<th.*?>(.*?)</th>', re.S)
        return [header.strip() for header in header_data_pattern.findall(header_row)]
    return []

# Regluleg segð til að finna viðeigandi línur (tr)
def parse_participant_rows(html):
    row_pattern = re.compile(r'<tr.*?>(.*?)</tr>', re.S)
    return row_pattern.findall(html)

# Regluleg segð til að finna dálkagögn (td)
def parse_participant_data(row):
    data_pattern = re.compile(r'<td.*?>(.*?)</td>', re.S)
    return [data.strip() for data in data_pattern.findall(row)]

# Regluleg segð til að finna kyn og aldur ef þau eru til staðar
def extract_gender_age(data):
    gender_age_pattern = re.compile(r'(\w+)?(?:, (\d+))?')
    match = gender_age_pattern.search(data)
    gender = match.group(1) if match and match.group(1) else 'N/A'
    age = match.group(2) if match and match.group(2) else 'N/A'
    return gender, age

def fetch_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Tókst ekki að sækja gögn af {url}")
        return None


def parse_html(html, idx):
    # Find the column headers in the HTML
    headers = parse_column_headers(html)
    if not headers:
        print("Ekki tókst að finna dálkaheiti.")
        return []

    # Find all participant rows in the HTML
    rows = parse_participant_rows(html)
    results = []

    # Define the column mapping from the HTML table to the SQLite table
    column_mapping = {
        'Rank': 'hlaup_id',  # Rank maps to hlaup_id
        'Name': 'nafn',      # Name maps to nafn
        'Time': 'timi',      # Time maps to timi
        'Year': 'aldur'      # Year maps to aldur
    }

    # Process each row and map to the correct structure
    for row in rows:
        columns = parse_participant_data(row)
        if len(columns) != len(headers):  # Ensure the number of columns matches the headers
            continue

        # Map the data to the correct structure for insertion into SQLite
        participant_data = {'id': idx}  # Assign id based on link index (idx)
        for header, value in zip(headers, columns):
            if header in column_mapping:
                participant_data[column_mapping[header]] = value.strip()

        # Handle the 'kyn' field (set to 'N/A' or NULL if not available)
        participant_data['kyn'] = 'N/A'  # You can set this to None if you want NULL in the database

        # Append the participant data to the results list
        results.append(participant_data)

    return results

# Fall til að skrifa niðurstöður í CSV-skrá
def skrifa_nidurstodur(data, output_file):
    """
    Skrifar niðurstöður í úttaksskrá.
    :param data:        (list) Listi af línum
    :param output_file: (str) Slóð að úttaksskrá
    :return:            None
    """
    if not data:
        print("Engar niðurstöður til að skrifa.")
        return

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Reorganize columns for the correct structure
    df = pd.DataFrame(data, columns=['id', 'hlaup_id', 'nafn', 'timi', 'kyn', 'aldur'])
    df.to_csv(output_file, sep=',', index=False)
    print(f"Niðurstöður vistaðar í '{output_file}'.")



def parse_race_metadata(html):
    # Finna nafn hlaupsins
    race_name_pattern = re.compile(
        r'<h1.*?>(.*?)</h1>|<title.*?>(.*?)</title>|<h2.*?>(.*?)</h2>|<div.*?class="race-name".*?>(.*?)</div>', re.S)
    race_name_match = race_name_pattern.search(html)

    if race_name_match:
        race_name = race_name_match.group(1) or race_name_match.group(2) or race_name_match.group(
            3) or race_name_match.group(4)
        race_name = race_name.strip()
    else:
        race_name = 'Unknown Race'

    # Finna upphafstíma (Start time)
    race_start_pattern = re.compile(r'<small class="stats-label">Start time</small>\s*<h4>(\d{2}:\d{2})</h4>', re.S)
    race_end_pattern = re.compile(r'<small class="stats-label">Est\. finish time</small>\s*<h4>(\d{2}:\d{2})</h4>',
                                  re.S)

    race_start_match = race_start_pattern.search(html)
    race_end_match = race_end_pattern.search(html)

    race_start = race_start_match.group(1).strip() if race_start_match else 'Unknown Start'
    race_end = race_end_match.group(1).strip() if race_end_match else 'Unknown End'

    # Finna fjölda þátttakenda (Started / Finished)
    participants_pattern = re.compile(
        r'<small class="stats-label">Started / Finished</small>\s*<h4>(\d+)\s*/\s*\d+</h4>', re.S)
    participants_match = participants_pattern.search(html)
    participants = participants_match.group(1).strip() if participants_match else 'Unknown Participants'

    # Auðkenni hlaups ef það er til (oft í URL eða skjölum)
    race_id_pattern = re.compile(r'race_id[:\-]\s*(\d+)', re.S)
    race_id_match = race_id_pattern.search(html)
    race_id = race_id_match.group(1).strip() if race_id_match else 'Unknown ID'

    # Skila metadata sem dictionary
    return {
        'id': race_id,
        'upphaf': race_start,
        'endir': race_end,
        'nafn': race_name,
        'fjoldi': participants
    }


def skrifa_metadata(output_file_base, idx, html):
    # Tryggja að mappan sem við ætlum að skrifa í sé til
    os.makedirs(os.path.dirname(output_file_base), exist_ok=True)

    # Fá metadata án URL og Downloaded At
    metadata = parse_race_metadata(html)

    # Set the id to be the index (idx)
    metadata['id'] = idx  # Assign id based on the index of the link

    # Write JSON file
    json_output_file = f"{output_file_base}.json"
    with open(json_output_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=4)
    print(f"Metadata vistað í '{json_output_file}'.")

    # Write CSV file
    csv_output_file = f"{output_file_base}.csv"
    df = pd.DataFrame([metadata])
    df.to_csv(csv_output_file, index=False)
    print(f"Metadata vistað í '{csv_output_file}'.")


def parse_arguments():
    parser = argparse.ArgumentParser(description='Vinna með úrslit af tímataka.net.')
    parser.add_argument('--links_file', help='Slóð að txt skrá með lista af hlekkjum.')
    parser.add_argument('--output_dir', required=True,
                        help='Slóð að möppu til að vista niðurstöðurnar (CSV format).')
    parser.add_argument('--debug', action='store_true',
                        help='Vistar html í skrá til að skoða.')
    parser.add_argument('--metadata_output_dir', required=False,
                        help='Slóð til að vista metadata í CSV eða JSON formi.')
    return parser.parse_args()

def main():
    args = parse_arguments()

    # Read all the links from the txt file
    if not args.links_file.endswith('.txt'):
        print(f"Inntaksskráin {args.links_file} þarf að vera txt skrá.")
        return

    links = read_links_from_file(args.links_file)

    # Create a debug folder if --debug is set
    if args.debug:
        debug_folder = './debug_files'
        os.makedirs(debug_folder, exist_ok=True)

    # Loop through each link and process it
    for idx, url in enumerate(links, start=1):  # Start idx from 1 (for link 1)
        print(f"Vinnur með hlekk: {url}")

        html = fetch_html(url)
        if not html:
            print(f"Ekki tókst að sækja HTML gögn fyrir hlekk: {url}")
            continue

        # Save HTML file in debug mode
        if args.debug:
            debug_file_path = f'{debug_folder}/debug_{idx}.html'
            with open(debug_file_path, 'w') as debug_file:
                debug_file.write(html)
            print(f"Debug HTML vistað í '{debug_file_path}'.")

        # Process the HTML and map the data
        results = parse_html(html, idx)  # Pass the link index as id

        # Define output file paths
        output_file = f"{args.output_dir}/results_{idx}.csv"
        metadata_output_base = f"{args.metadata_output_dir}/metadata_{idx}" if args.metadata_output_dir else None

        # Write the results to a CSV file
        skrifa_nidurstodur(results, output_file)

        # Write metadata if the output directory is provided
        if metadata_output_base:
            skrifa_metadata(metadata_output_base, idx, url, html)



if __name__ == "__main__":
    main()

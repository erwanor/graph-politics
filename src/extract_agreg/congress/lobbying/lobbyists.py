from utils import get_path, get_crd, read_file
import sys
import uuid
import csv

csv.field_size_limit(sys.maxsize)

CRD_PATH = get_crd(__file__)
DATASET_PATH_TO = {
    'LOBBYISTS':
    get_path(CRD_PATH, '/../../../../datasets/raw/Congress/Lobby/lob_lobbyist.txt'),
    'LOBBYING_FIRMS':
    get_path(CRD_PATH, '/../../../../datasets/processed/lobbying/firms.csv')
}

OUTPUT_PATH = {
    'LOBBYISTS_STORE':
    get_path(CRD_PATH, '/../../../../datasets/processed/lobbying/lobbyists_store.csv'),
    'LOBBYISTS_DATA':
    get_path(CRD_PATH, '/../../../../datasets/processed/lobbying/lobbyists_data.csv')
}


def create_lobbyist(cleaned_data, lobbyists_store, lobbying_firms):
    """
	Return a dictionnary of bundled data from the lobbying firms and lobbyists stores.
	"""
    SOPR = cleaned_data[0]
    full_name = cleaned_data[2]
    lobbyist_id = cleaned_data[3]

    if lobbyists_store.has_key(lobbyist_id):
        CUID = lobbyists_store[lobbyist_id]
    else:
        CUID = str(uuid.uuid4())

    year = cleaned_data[4]
    former_congressmen = cleaned_data[-1]

    if lobbying_firms.has_key(SOPR) is True:
        CUID_employer = lobbying_firms[SOPR]
    else:
        CUID_employer = 0

    return {
        'CUID_lobbyist': CUID,
        'CUID_employer': CUID_employer,
        'lobbyist_id': lobbyist_id,
        'lobbyist_name': full_name,
        'former_congressmen': former_congressmen,
        'record_year': year
    }


def from_dataset_index_by(csv_file,
                          key_i,
                          value_i,
                          delimiter='|',
                          quoting=csv.QUOTE_NONE):
    """
	Read and parse a csv_file and index the value_i-th column by the key_i-th column.
	Return a dictionnary
	"""
    store = {}
    with open(csv_file, 'rb') as f:
        reader = csv.reader(f, delimiter=delimiter, quoting=quoting)
        for entry in reader:
            entry = filter(lambda x: x != '' and x != ',', entry)
            key = entry[key_i]
            value = entry[value_i]
            if store.has_key(key):
                store[key].append(value)
            else:
                store[key] = [value]
    return store


def generate_lobbyists():
    """
	Generate a mapping of LID to CUID and prepare rows to be written to csv.
	Return a list of rows and a dictionnary.
	"""
    all_rows = []
    lobbyists = {}
    SOPR_store = from_dataset_index_by(DATASET_PATH_TO['LOBBYISTS'], 3, 0)
    for LID in SOPR_store.keys():
        CUID_lobbyist = str(uuid.uuid4())
        lobbyists[LID] = CUID_lobbyist

        values = SOPR_store[LID]
        SOPR_store[LID] = ';'.join(values)
        row = [CUID_lobbyist, LID, SOPR_store[LID]]
        all_rows.append(row)

    return (all_rows, lobbyists)


def csv_write(data_entries, OUTPUT_FILE, fieldnames=[]):
    """
	Write processed data to a CSV file on disk.
	"""
    with open(OUTPUT_FILE, 'wb') as output:
        if type(data_entries[0]) is dict:
            writer = csv.DictWriter(
                output,
                fieldnames=fieldnames,
                delimiter='%',
                quoting=csv.QUOTE_NONE,
                escapechar='\\')
            writer.writeheader()
            for entry in data_entries:
                writer.writerow(entry)
        else:
            writer = csv.writer(
                output, delimiter='%', quoting=csv.QUOTE_NONE, escapechar='\\')
            writer.writerow(fieldnames)
            writer.writerows(data_entries)
    return


def map_SOPR_to_firm():
    """
	Map SOPR identifiers to a lobbying CUID.
	Return a dictionnary.
    """
    firms = {}
    with open(DATASET_PATH_TO['LOBBYING_FIRMS'], 'rb') as f:
        reader = csv.reader(f, delimiter='%', quoting=csv.QUOTE_NONE)
        for record in reader:
            SOPR_reports = record[3].split(';')
            CUID_firm = record[0]
            for report_id in SOPR_reports:
                firms[report_id] = CUID_firm
    return firms

def is_a_duplicate(tracking_store, key_to_check):
    return tracking_store.has_key(key_to_check)


def process_lobbyists(raw_lines, lobbyists_store, lobbying_firms):
    """
	Process raw data and return a list of dictionnaries that are ready to be written to a CSV
	"""
    all_lobbyists = []
    tracking = {}
    for line in raw_lines:
        if len(line) < 5:
            continue

        data = [v for (k, v) in enumerate(line.split('|')) if k % 2 != 0]
        lobbyist = create_lobbyist(data, lobbyists_store, lobbying_firms)

        if is_a_duplicate(tracking, data[3]) is True:
            continue
        else:
            tracking[data[3]] = True
            all_lobbyists.append(lobbyist)

    return all_lobbyists

# Overview:
# 0. Map lobbyists LIDs (Lobbyist IDentifiers) to CUIDs (Cross-data Unique IDentifiers)
# 1. Prepare the rows of the csv lobbyist store
# 2. Map SOPR report ids to lobbying firms CUIDs
# 3. Process the lobbyist data and detect connections between firms, lobbyists and SOPR reports
# 4. Load that data into a CSV file
####

lobbyists_data, lobbyists_store = generate_lobbyists()
csv_write(lobbyists_data, OUTPUT_PATH['LOBBYISTS_STORE'],
          ['CUID_lobbyist', 'lobbyist_id', 'SOPR_reports'])

raw = read_file(DATASET_PATH_TO['LOBBYISTS'])
firms_by_SOPR = map_SOPR_to_firm()
processed_data = process_lobbyists(raw, lobbyists_store, firms_by_SOPR)

fieldnames = [
    "CUID_lobbyist", "CUID_employer", "lobbyist_id", "lobbyist_name",
    "former_congressmen", "record_year"
]
csv_write(processed_data, OUTPUT_PATH['LOBBYISTS_DATA'], fieldnames)

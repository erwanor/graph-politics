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

# Overview:
# 0. Map lobbyists LIDs (Lobbyist IDentifiers) to CUIDs (Cross-data Unique IDentifiers)
# 1. Prepare the rows of the csv lobbyist store
# 2. Map SOPR report ids to lobbying firms CUIDs
# 3. Process the lobbyist data and detect connections between firms, lobbyists and SOPR reports
# 4. Load that data into a CSV file
####

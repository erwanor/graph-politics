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

# Overview:
# 0. Map lobbyists LIDs (Lobbyist IDentifiers) to CUIDs (Cross-data Unique IDentifiers)
# 1. Prepare the rows of the csv lobbyist store
# 2. Map SOPR report ids to lobbying firms CUIDs
# 3. Process the lobbyist data and detect connections between firms, lobbyists and SOPR reports
# 4. Load that data into a CSV file
####

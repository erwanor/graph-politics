from utils import get_path, get_crd, read_file
import uuid
import csv

CRD_PATH = get_crd(__file__)
DATASET_PATH_TO = {
    'AGENCIES_LOBBIED':
    get_path(CRD_PATH, '/../../../../datasets/raw/Congress/Lobby/lob_agency.txt'),
    'LOBBYING': 
    get_path(CRD_PATH, '/../../../../datasets/raw/Congress/Lobby/fixed_lob_lobbying.txt'),
    'LOBBYISTS':
    get_path(CRD_PATH, '/../../../../datasets/raw/Congress/Lobby/lob_lobbyist.txt')
}

OUTPUT_PATH = {
    'LOBBYING_FIRMS':
    get_path(CRD_PATH, '/../../../../datasets/processed/lobbying/firms.csv'),
    'LOBBYING_CLIENTS':
    get_path(CRD_PATH, '/../../../../datasets/processed/lobbying/index_clients.csv'),
    'TRANSACTIONS': 
    get_path(CRD_PATH, '/../../../../datasets/processed/lobbying/transactions.csv')
}

FIELDS = {
    'LOBBYING_FIRMS':
    ["CUID_lobby", "lobby_name", "CUID_clients", "SOPRs", "is_firm"],
    'LOBBYING_CLIENTS':
    ["CUID_corp", "corp_name", "lobbying_agencies_hired", "SOPRs"],
    'TRANSACTIONS': ["CUID_corp", "CUID_lobby", "amount_paid"]
}


def preprocess_entry(raw_line):
    split = raw_line.split('|')
    return [value for index, value in enumerate(split) if index % 2 != 0]


def clean_lob_lobbying(raw_line):
    cleaned = []
    split_raw = raw_line.split('|')
    for index, entry in enumerate(split_raw):
        if index % 2 == 0 or len(split_raw) <= 1:
            continue
        else:
            cleaned.append(entry)
    return cleaned[:-9]


def create_firm(lobbying_store, data):
    CUID_lobby = str(uuid.uuid4())
    lobby_name = data[2]
    lobbying_firm = {
        'CUID_lobby': CUID_lobby,
        'lobby_name': lobby_name,
        'SOPRs': [],
        'CUID_clients': []
    }
    lobbying_store[lobby_name] = lobbying_firm
    return lobbying_store


def create_corp(corps_store, corp_name):
    CUID_corp = str(uuid.uuid4())
    corporation = {
        'CUID_corp': CUID_corp,
        'corp_name': corp_name,
        'SOPRs': [],
        'lobbying_agencies_hired': []
    }
    corps_store[corp_name] = corporation
    return corps_store


def update_stores(record, lobbying_firms, corporations, transactions):
    SOPR_id = record[0]
    lobby_name = record[2]
    client = record[4]
    amount_paid = record[7]

    if lobbying_firms.has_key(lobby_name) is False:
        lobbying_firms = create_firm(lobbying_firms, record)
    lobbying_firms[lobby_name]['SOPRs'].append(SOPR_id)
    CUID_lobby = lobbying_firms[lobby_name]['CUID_lobby']
    lobby_clients = lobbying_firms[lobby_name]['CUID_clients']

    if corporations.has_key(client) is False:
        corporations = create_corp(corporations, client)
    corporations[client]['SOPRs'].append(SOPR_id)
    corporations[client]['lobbying_agencies_hired'].append(CUID_lobby)
    CUID_corp = corporations[client]['CUID_corp']

    if amount_paid is not "0.0":
        transactions.append((CUID_corp, CUID_lobby, amount_paid))
        lobbying_firms[lobby_name]['CUID_clients'].append(CUID_corp)

    return (lobbying_firms, corporations, transactions)


def extract_lobbying(raw, lobbying_firms, corporations, transactions):
    preprocessed = [preprocess_entry(record) for record in raw]
    preprocessed = filter(lambda x: len(x) >= 8, preprocessed)
    for entry in preprocessed:
        lobbying_firms, corporations, transactions = update_stores(
            entry, lobbying_firms, corporations, transactions)
    return (lobbying_firms, corporations, transactions)


def collapse(store, key, subkey):
    return ';'.join(store[key][subkey])


def prepare(dict_stores):
    for store in dict_stores:
        if type(store) is not dict: continue
        for key in store.keys():
            for subk in store[key].keys():
                if type(store[key][subk]) is list:
                    store[key][subk] = collapse(store, key, subk)
    return dict_stores


def csv_write(output, data, fieldnames=[]):
    with open(output, 'wb') as fout:
        if type(data) is dict:
            writer = csv.DictWriter(
                fout,
                fieldnames=fieldnames,
                delimiter='%',
                quoting=csv.QUOTE_NONE,
                escapechar='\\')
            writer.writeheader()
        else:
            writer = csv.writer(
                fout, delimiter='%', quoting=csv.QUOTE_NONE, escapechar='\\')
            writer.writerow(fieldnames)
        for entry in data:
            to_write = entry if type(data) is list else data[entry]
            writer.writerow(to_write)
    return


lobbying_firms = {}
corporations = {}
transactions = []

raw_lines = read_file(DATASET_PATH_TO['LOBBYING'])
aggregated_data = extract_lobbying(raw_lines, lobbying_firms, corporations,
                                   transactions)
ready_to_write = prepare(aggregated_data)

csv_write(
    OUTPUT_PATH['LOBBYING_FIRMS'],
    ready_to_write[0],
    fieldnames=FIELDS['LOBBYING_FIRMS'])
csv_write(
    OUTPUT_PATH['LOBBYING_CLIENTS'],
    ready_to_write[1],
    fieldnames=FIELDS['LOBBYING_CLIENTS'])
csv_write(
    OUTPUT_PATH['TRANSACTIONS'],
    ready_to_write[2],
    fieldnames=FIELDS['TRANSACTIONS'])

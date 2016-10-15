import os
import yaml
import csv

CRD_PATH = os.path.dirname(os.path.realpath(__file__))
CURRENT_COMMITTEE_MEMBERS = ''.join([
    CRD_PATH,
    '/../../../../datasets/raw/Legislators/Congressional_committees/committee-membership-current.yaml'
])
INDEX_BY_BIO_UID = ''.join([
    CRD_PATH,
    '/../../../../datasets/preprocessed/legislators_BIO_UID_to_CUID.csv'
])
OUTPUT_COMMITTEE_MEMBERS = ''.join([
    CRD_PATH,
    '/../../../../datasets/preprocessed/congressional_committees_current_members.csv'
])


def preproc_yaml(parsed_yaml, uid_store):
    to_process = []
    for committee_thomas_id in parsed_yaml:
        for members in parsed_yaml[committee_thomas_id]:
            BIO_UID = members['bioguide']
            if uid_store.has_key(BIO_UID) is True:
                CUID = uid_store[BIO_UID]
            else:
                continue  # committee member is no longer serving (deceased, retired or else.)
            if members.has_key('title'):
                position = members['title']
            else:
                position = ''
            member = {
                'CUID_member': CUID,
                'BIO_UID': BIO_UID,
                'thomas_id': committee_thomas_id,
                'position': position
            }

            to_process.append(member)

    return to_process


def csv_extract(INPUT_PATH):
    store = {}
    with open(INPUT_PATH, 'rb') as srcfile:
        reader = csv.reader(srcfile, delimiter='%', quoting=csv.QUOTE_NONE)
        for entry in reader:
            store.update({entry[0]: entry[1]})
    return store


def process_to_csv(to_process, OUTPUT_PATH, fieldnames):
    with open(OUTPUT_PATH, 'wb') as output:
        writer = csv.DictWriter(
            output,
            fieldnames=fieldnames,
            delimiter='%',
            quoting=csv.QUOTE_NONE)
        writer.writeheader()
        for entry in to_process:
            writer.writerow(entry)


with open(CURRENT_COMMITTEE_MEMBERS, 'r') as srcfile:
    try:
        parsed_yaml = yaml.load(srcfile)
    except yaml.YAMLError as exc:
        print(exc)

uid_store = csv_extract(INDEX_BY_BIO_UID)
to_process = preproc_yaml(parsed_yaml, uid_store)

fieldnames = ["CUID_member", "BIO_UID", "thomas_id", "position"]
process_to_csv(to_process, OUTPUT_COMMITTEE_MEMBERS, fieldnames)

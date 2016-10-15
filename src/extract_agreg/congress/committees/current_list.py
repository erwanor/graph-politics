import os
import yaml
import uuid
import csv

CRD_PATH = os.path.dirname(os.path.realpath(__file__))
CURRENT_COMMITTEES = ''.join([
    CRD_PATH,
    '/../../../../datasets/raw/Legislators/Congressional_committees/committees-current.yaml'
])
CURRENT_COMMITTEE_MEMBERS = ''.join([
    CRD_PATH,
    '/../../../../datasets/raw/Legislators/Congressional_committees/committee-membership-current.yaml'
])
OUTPUT_LIST_COMMITTEES = ''.join([
    CRD_PATH,
    '/../../../../datasets/processed/congress/committees/list_114th.csv'
])
OUTPUT_STORE_COMMITTEE_IDS = ''.join([
    CRD_PATH,
    '/../../../../datasets/processed/congress/committees/ids_114th.csv'
])

com_store = {}


def chamber_name(abrv):
    if abrv == "senate":
        return "Senate"
    else:
        return "House of Representatives"


def gather_committee_cuids(committees):
    cuids = []
    for entry in committees:
        cuids.append(entry['CUID_committee'])
    return cuids


def preproc_yaml(parsed_yaml, chamber=None, is_subcom=False, prefix_tid=""):
    to_process = []
    for entry in parsed_yaml:
        CUID = str(uuid.uuid4())
        name = entry['name']
        children = []
        thomas_id = ''.join([prefix_tid, entry['thomas_id']])

        if entry.has_key('type') is True:
            chamber = chamber_name(entry['type'])

        if entry.has_key('subcommittees') is True:
            children = preproc_yaml(
                entry['subcommittees'],
                chamber=chamber,
                is_subcom=True,
                prefix_tid=thomas_id)
            subcom_ids = gather_committee_cuids(children)
        else:
            subcom_ids = ''

        committee = {
            'CUID_committee': CUID,
            'committee_name': name,
            'children': ';'.join(subcom_ids),
            'chamber': ''.join([chamber]),
            'is_subcom': int(is_subcom),
            'thomas_id': thomas_id
        }

        to_process.append(committee)
        to_process.extend(children)

    return to_process


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


def generate_uid_store(to_process):
    for entry in to_process:
        for key in entry.keys():
            if key != "CUID_committee" and key != "thomas_id":
                del entry[key]
    return to_process


with open(CURRENT_COMMITTEES, 'r') as srcfile:
    try:
        parsed_yaml = yaml.load(srcfile)
    except yaml.YAMLError as exc:
        print(exc)

to_process = preproc_yaml(parsed_yaml)

fieldnames = [
    "CUID_committee", "thomas_id", "chamber", "committee_name", "children",
    "is_subcom"
]
process_to_csv(to_process, OUTPUT_LIST_COMMITTEES, fieldnames)

to_process = generate_uid_store(to_process)

fieldnames = ["thomas_id", "CUID_committee"]
process_to_csv(to_process, OUTPUT_STORE_COMMITTEE_IDS, fieldnames)

import os
import csv
import uuid
import csv

CRD_PATH = os.path.dirname(os.path.realpath(__file__))
CURRENT_LEGISLATORS = ''.join([CRD_PATH, '/../../datasets/raw/Legislators/CSV/legislators-current.csv'])

OUTPUT_LEGISLATOR_DATA = ''.join([CRD_PATH, '/../../datasets/preprocessed/current_legislators.csv'])
OUTPUT_UID_STORE_BY_BIO_UID = ''.join([CRD_PATH, '/../../datasets/preprocessed/legislators_BIO_UID_to_CUID.csv'])

def chamber_name(abrv):
	if abrv == "sen":
		return "Senate"
	elif abrv == "rep":
		return "House of Representatives"
	else:
		return "Official"

def contains_digits(string):
	if string == '':
		return False
	else:
		return string[0].isdigit() or contains_digits(string[1:])

def congressman(CUID, full_name, last_name, first_name, dob, sex, state, party, chamber, OS_UID, GOVTrack_UID, CSPAN_UID, BIO_UID):
	"""Bundle data about a given congressmen - returns a tuple of dicts containing the bundled data
	and a dict indexed by CUIDs containing the other UIDs used by various datasources"""
	if len(full_name) == 0 or contains_digits(full_name) is True:
		full_name = first_name + ' ' + last_name
	data = { 'full_name'       : full_name,
		'first_name'       : first_name,
		'last_name'        : last_name,
		'dob'              : dob,
		'sex'              : sex,
		'party'            : party,
		'state'            : state,
		'chamber'          : chamber_name(chamber),
		'CUID_legislator'  : CUID,
		'OS_UID'           : OS_UID,
		'GOVTRACK_UID'     : GOVTrack_UID,
		'CSPAN_UID'        : CSPAN_UID,
		'BIO_UID'          : BIO_UID }
	return (data, { 'BIO_UID' : BIO_UID, 'CUID' : CUID })

def write_and_dump(data_to_dump, OUTPUT_PATH, fieldnames):
	with open(OUTPUT_PATH, 'wb') as output:
		writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter='%', quoting=csv.QUOTE_NONE)
		writer.writeheader()
		for entry in data_to_dump:
			writer.writerow(entry)
		

legislators = [] 
index_by_BIO_UID = []

with open(CURRENT_LEGISLATORS, 'rb') as srcfile:
	parsed_csv = csv.reader(srcfile)
	for entry in parsed_csv:
		CUID         = str(uuid.uuid4())
		full_name    = entry[25]
		last_name    = entry[0]
		first_name   = entry[1]
		dob          = entry[2]
		sex          = entry[3]
		state        = entry[5]
		party        = entry[7]
		chamber      = entry[4]
		OS_UID       = entry[20]
		GOVTRACK_UID = entry[22]
		CSPAN_UID    = entry[23]
		BIO_UID      = entry[18]

		congressman_data, uids_by_BIO_UID = congressman(CUID, full_name, last_name, first_name, 
								dob, sex, state, party, chamber, OS_UID, 
								GOVTRACK_UID, CSPAN_UID, BIO_UID)

		legislators.append(congressman_data)
		index_by_BIO_UID.append(uids_by_BIO_UID)

index_by_BIO_UID.pop(0) # Remove header from imported csv

fieldnames = ["CUID_legislator", "full_name", "first_name", "last_name", "chamber", "state", "party", "dob", "sex",
		"OS_UID", "CSPAN_UID", "GOVTRACK_UID", "BIO_UID"]
write_and_dump(legislators, OUTPUT_LEGISLATOR_DATA, fieldnames)
write_and_dump(index_by_BIO_UID, OUTPUT_UID_STORE_BY_BIO_UID, ["BIO_UID", "CUID"])

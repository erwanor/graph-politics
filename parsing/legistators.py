import os
import json

CRD_PATH           = os.path.dirname(os.path.realpath(__file__))
LEGISLATOR_DATASET = ''.join([CRD_PATH, '/../datasets/congress/legislators_excerpt.json'])

def create_legislator(first, last, chamber, state, party, fec_id):
	return {'FEC_ID'     : fec_id,
		'first_name' : first,
		'last_name'  : last,
		'chamber'    : chamber,
		'party'      : party,
		'state'      : state}
	
with open(LEGISLATOR_DATASET, 'r') as src_file:
	json_string = src_file.read().replace('\n', '')

parsed_legislators = json.loads(json_string)
house    = []
senate   = []
special  = []

for legislator in parsed_legislators['results']:
	to_json = create_legislator(legislator['first_name'],
				    legislator['last_name'], 
				    legislator['chamber'], 
				    legislator['state'],
				    legislator['party'],
				    legislator['fec_ids'][0])
	if legislator['chamber'] == "house":
		house.append(to_json)
	elif legislator['chamber'] == "senate":
		senate.append(to_json)
	else:
		other.append(to_json)

json_to_encode = { 'house'   : house,
		   'senate'  : senate,
		   'special' : special }
print json.dumps(json_to_encode)

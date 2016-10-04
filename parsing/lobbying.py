import os
import json

CRD_PATH           = os.path.dirname(os.path.realpath(__file__))

def get_path(path_to_dataset):
	return ''.join([CRD_PATH, path_to_dataset])

def read_file_by_line(path):
	with open(path, 'r') as srcfile:
		lines = srcfile.read().split('\n')
	return lines

def create_lobbying_agency(category, target, lobbyists):
	return { 'category': category, 'target': target, 'lobbyists': lobbyists }

def process_agencies(lobbying_data):
	lines = read_file_by_line(LOBBYING_AGENCY_DATASET)
	lines.pop()

	for line in lines:
		parsed_data 	= line.split('|')
		lobbying_info   = create_lobbying_agency(parsed_data[3][:-1], parsed_data[5], [])
		lobbying_data.update( { parsed_data[1]: lobbying_info })
	return lobbying_data

def process_lobbyists(lobbying_data):
	lines = read_file_by_line(LOBBYIST_DATASET)
	lines.pop()

	for line in lines:
		parsed_data	= line.split('|')
		if len(parsed_data) <= 1:
			continue

		lobbyist_agency = parsed_data[1]
		lobbyist_name   = parsed_data[3].split(', ')

		if len(lobbyist_name) < 2:
			# Noise in the dataset
			continue
		else:
			lobbyist_name   = ''.join([lobbyist_name[1], ' ', lobbyist_name[0]])

		if lobbying_data.has_key(lobbyist_agency) is not True:
			lobbying_data.update({ lobbyist_agency: create_lobbying_agency('000', '', [])})
		lobbying_data[lobbyist_agency]['lobbyists'].append(lobbyist_name.title())
	return lobbying_data

LOBBYING_AGENCY_DATASET = get_path('/../datasets/lobbying/lob_agency.txt')
LOBBYIST_DATASET 	= get_path('/../datasets/lobbying/lob_lobbyist.txt')
LOBBYING_MAIN		= get_path('/../datasets/lobbying/lob_lobbying.txt')

lobbying_data = process_agencies({})
lobbying_data = process_lobbyists(lobbying_data)

json_to_dump  = { 'lobbying': [lobbying_data] }
dumped        = json.dumps(json_to_dump, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)

print unicode(dumped, errors='ignore')

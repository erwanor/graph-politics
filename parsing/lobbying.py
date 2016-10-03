import os
import json

CRD_PATH           = os.path.dirname(os.path.realpath(__file__))

def get_path(path_to_dataset):
	return ''.join([CRD_PATH, path_to_dataset])
def process_lobbyists(lobbying_data):
	lines = read_file_by_line(LOBBYST_DATASET)
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
LOBBYST_DATASET 	= get_path('/../datasets/lobbying/lob_lobbyist.txt')
LOBBYING_CLIENT		= get_path('/../datasets/lobbying/lob_lobbying.txt')

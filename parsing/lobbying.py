import os
import json

CRD_PATH           = os.path.dirname(os.path.realpath(__file__))

def get_path(path_to_dataset):
	return ''.join([CRD_PATH, path_to_dataset])
LOBBYING_AGENCY_DATASET = get_path('/../datasets/lobbying/lob_agency.txt')
LOBBYST_DATASET 	= get_path('/../datasets/lobbying/lob_lobbyist.txt')
LOBBYING_CLIENT		= get_path('/../datasets/lobbying/lob_lobbying.txt')

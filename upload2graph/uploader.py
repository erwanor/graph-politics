from neo4j.v1 import GraphDatabase, basic_auth
import os
import json

CRD_PATH              = os.path.dirname(os.path.realpath(__file__))
CONGRESS_LIST_DATASET = ''.join([CRD_PATH, '/../processed_data/congress/congress_list_excerpt.json'])

def store_file_in_memory(path):
	with open(path, 'r') as srcfile:
		file_string = srcfile.read().replace('\n', '')
	return file_string

def chamber_noun(chamber):
	if chamber == 'house':
		return 'Representative'
	elif chamber == 'senate':
		return 'Senator'
	else:
		return 'Official'

def party_name(abr):
	if abr == 'R':
		return 'Republican'
	elif abr == 'D':
		return 'Democrat'
	else:
		return 'Independent'

def remove_redundant_entries(politician):
	del politician['chamber']
	del politician['party']
	del politician['state']
	return

db_username = os.environ["NEO4J_USERNAME"]
db_password = os.environ["NEO4J_PASSWORD"]
db_server   = os.environ["NEO4J_SERVER_URI"]


session.close()

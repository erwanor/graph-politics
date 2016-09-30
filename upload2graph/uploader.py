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

def format_dict_to_str(hashtable):
	string = '{'
	for k in hashtable:
		string = ''.join([string, k, ':', '"', hashtable[k], '"', ','])
	string = ''.join([string[:-1], '}'])
	return string

def upload_congress(session):
	congress_json = store_file_in_memory(CONGRESS_LIST_DATASET)
	congress_data = json.loads(congress_json)
	for chamber in congress_data:
		for politician in congress_data[chamber]:
			chamber_cap = chamber_noun(chamber)
			party       = party_name(politician['party'])
			state       = politician['state']
			remove_redundant_entries(politician)
			politician_str = format_dict_to_str(politician)
			CYPHER_QUERY = ''.join(['CREATE (n: Politician:Congress:', chamber_cap, ':', party, politician_str, ')'])
			session.run(CYPHER_QUERY)
	return

db_username = os.environ['NEO4J_USERNAME']
db_password = os.environ['NEO4J_PASSWORD']
db_server   = os.environ['NEO4J_SERVER_URI']

driver  = GraphDatabase.driver(db_server, auth = basic_auth(db_username, db_password))
session = driver.session()

upload_congress(session)

session.close()

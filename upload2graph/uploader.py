from neo4j.v1 import GraphDatabase, basic_auth
import os

CRD_PATH      = os.path.dirname(os.path.realpath(__file__))
CONGRESS_LIST = ''.join([CRD_PATH, '/../processed_data/congress/legislators_excerpt.json'])

def upload_congress():
	return

db_username = os.environ["NEO4J_USERNAME"]
db_password = os.environ["NEO4J_PASSWORD"]
db_server   = os.environ["NEO4J_SERVER_URI"]

driver = GraphDatabase.driver(db_server, auth = basic_auth(db_username, db_password))

session.close()

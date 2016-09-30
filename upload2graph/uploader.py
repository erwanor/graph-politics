from neo4j.v1 import GraphDatabase, basic_auth
import os

db_username = os.environ["NEO4J_USERNAME"]
db_password = os.environ["NEO4J_PASSWORD"]
db_server   = os.environ["NEO4_SERVER_URI"]

driver = GraphDatabase.driver(db_server, auth = basic_auth(db_username, db_password))

session.close()

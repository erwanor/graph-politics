from py2neo  import authenticate as graph_db_auth, Graph, Node, Relationship
from os      import environ as env_vars
from os.path import dirname, realpath
from uuid    import uuid4
import json

# Generate path to dataset using the current reading diretory's realpath
CRD_PATH              = dirname(realpath(__file__))
CONGRESS_LIST_DATASET = ''.join([CRD_PATH, '/../processed_data/congress/congress_list_excerpt.json'])
LOBBYING_DATASET      = ''.join([CRD_PATH, '/../processed_data/lobbying/lobbying_data.json'])

# Graph database authentication infos are stored in environment variables
NEO4J_SERVER_PORT = ':'.join([env_vars['NEO4J_SERVER_NAME'], env_vars['NEO4J_SERVER_PORT']])
NEO4J_DB_USERNAME = env_vars['NEO4J_DB_USERNAME']
NEO4J_DB_PASSWORD = env_vars['NEO4J_DB_PASSWORD']

def store_file_in_memory(path):
	'''Store file content in memory and in a single line'''
	with open(path, 'r') as srcfile:
		file_string = srcfile.read().replace('\n', '')
	return file_string

def check_whitespace(string):
	'''Add double quotes to string containing whitespaces'''
	add_double_quotes = False
	for char in string:
		if char == ' ':
			add_double_quotes = True
	if add_double_quotes is True:
		return ''.join(['"', string, '"'])
	else:
		return string

def chamber_name(chamber):
	'''Capitalize chamber names'''
	if chamber == 'house':
		return 'House of Representatives'
	elif chamber == 'senate':
		return 'Senate'
	else:
		return 'Official'

def party_name(abrv):
	'''Replace party abreviation by full party name'''
	if abrv == 'R':
		return 'Republican'
	elif abrv == 'D':
		return 'Democrat'
	else:
		return 'Independent'

	return

def clear_graph(graph):
	'''Delete all nodes and relationships from the graph databse'''
	QUERY_QUEUE = ['MATCH (n)-[r]-() DELETE n,r', 'MATCH (n) DELETE n']
	for CYPHER_QUERY in QUERY_QUEUE:
		graph.run(CYPHER_QUERY)
	print 'Cleared graph'
	return

def main_political_nodes(roots, graph):
	'''Create main political nodes/relationships; graph building blocks'''
	store = {}
	for entry in roots:
		# Store references to the node objects we create
		# They will be re-used to create relationships
		store.update({ entry[1]: Node(entry[0], name=entry[1]) })
		graph.create(store[entry[1]])
		print 'Create Node -  ', entry[0], ':', entry[1]

	graph.create(Relationship(store['Senate'], 'IS_A_CHAMBER_OF', store['Congress']))
	graph.create(Relationship(store['House of Representatives'], 'IS_A_CHAMBER_OF', store['Congress']))
	return store

def build_congress(root_nodes, graph):
	'''Generate congress nodes/relationships from the congress list dataset'''
	congress_json = store_file_in_memory(CONGRESS_LIST_DATASET)
	congress_data = json.loads(congress_json)
	# Hacky #######
	P_UID = 0
	# TO REMOVE ###
	for chamber in congress_data:
		for politician in congress_data[chamber]:
			#P_UID = RANDOM
			P_UID = P_UID + 1
			firstName      = politician['first_name']
			lastName       = politician['last_name']
			fullName       = ' '.join([firstName, lastName])
			chamberName    = chamber_name(chamber)
			partyName      = party_name(politician['party'])
			politicianNode = Node('Politician', full_name=fullName, PUID=P_UID)
			graph.create(politicianNode)
			graph.create(Relationship(politicianNode, 'MEMBER_OF', root_nodes[chamberName]))
			graph.create(Relationship(politicianNode, 'MEMBER_OF', root_nodes['Congress']))
			graph.create(Relationship(politicianNode, 'MEMBER_OF', root_nodes[partyName]))
	return

def build_lobbying(root_nodes, graph):
	'''Generate lobbying nodes/relationships from the lobbying dataset'''
	lobbying_json = store_file_in_memory(LOBBYING_DATASET)
	lobbying_data = json.loads(lobbying_json)
	for agencies in lobbying_data['agencies']:
		for uniqId in agencies:
			if agencies[uniqId].has_key('agency_name') is False:
				agency_name = 'Unknown'
			else:
				agency_name      = agencies[uniqId]['agency_name']
			agency_cat       = agencies[uniqId]['category']
			agency_target    = agencies[uniqId]['target']
			agency_lobbyists = agencies[uniqId]['lobbyists']

			agencyNode       = Node('Lobbying Agency', name=agency_name, LUID=uniqId, category=agency_cat)
			graph.create(agencyNode)
			
			for employee in agency_lobbyists:
				employeeNode = Node('Lobbyist', full_name=employee)
				graph.create(employeeNode)
				graph.create(Relationship(employeeNode, 'WORKS_FOR', agencyNode))
	return

POLITICAL_NODES = [('Institution', 'Congress'), ('Chamber', 'Senate'),
		('Chamber', 'House of Representatives'), 
		('Party', 'Republican'), ('Party', 'Democrat'),
		('Party', 'Independent')]

graph_db_auth(NEO4J_SERVER_PORT, NEO4J_DB_USERNAME, NEO4J_DB_PASSWORD)
graph = Graph()
clear_graph(graph)

root_nodes = main_political_nodes(POLITICAL_NODES, graph)
build_congress(root_nodes, graph)
build_lobbying([], graph)

# graph-politics

A semantic network reprensenting various connections between US politicians/Congresspeople (and their declared financial assets, liabilities, campaign expenditures and voting history) and private entities such as companies, lobbyist and special interest groups, non-profits, PACs.

### Data sources:

The US Government Open Data Initiative, the Federal Election Comission (FEC), Wikileaks and various public registries for which I am building scrappers.

### Objective:

Once the data has been retrieved, parsed and processed I upload it to a Neo4j graph database against which it is possible to run queries in order to extract interesting graph cycles and perhaps uncover conflict of interests. Another goal I have in mind is to research if the current political nomenclature (Republicans v. Democrats) is actually relevant to the contemporary political landscapes. Or if by analysing politicians voting patterns and funding networks we can clusterize them into categories that transcend the conventional partition Reps v. Dems.

At a later stage, I intend to work with the Stanford CoreNLP library to classify the stance that takes the lobbying groups working on a given US Bill. 

This is a "toy-project" that I have started because I have an interest in big data information retrieval, graph databases and semantic networks. My work is published under an MIT licence and might interest data journalists or concerned citizens.

### Directory structure

 - datasets/ : raw data about congress (name, party affiliation, bill (co-) sponsored, voting history etc.), registered lobbying agencies (their employees, expenditures, targets and bills)
 - processed_data/ : data that is ready to be uploaded to the graph db
- parsing/ : scripts used to process the raw datasets; reads from datasets/* and outputs to processed_data/
 - upload2graph/ : scripts to create nodes/relationships in the db; reads from processed_data/
 - env/ : configuration scripts
 - fraud_detection/ : algorithms run on the semantic network to extract/match cyclic patterns

#### Early-stage example:
![Congress](https://i.imgur.com/UI7Jeiy.png "An excerpt of a graph representing basic connections between congressmen and their political parties and office")
![CongressAndLobbying](https://i.imgur.com/V3b5zYY.png "Congressmen, lobbyists and parties")
![Lobbying](https://i.imgur.com/vzWIZZC.jpg "Lobbying agencies and their employees")


#### Some metrics:

Number of vertices (nodes) in our graph as of October 4th. 2016

 - MATCH (n) RETURN COUNT(n): 3,314,779 nodes
 
Number of edges (relationships) in our graph as of October 4th. 2016:

- MATCH ()-[r]-() RETURN COUNT(r): 4,608,010

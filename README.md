# graph-politics


A semantic network aggregating various datasources to represent the connections between US legislators - their assets, liabilities, campaign expenditures and supporters, funding networks and voting history - and private organizations such as corporations, lobbying agencies, 527 committees, [Super]PACs etc.

### Data sources:

The Federal Election Commission (FEC), the Center for Responsive Politics (CRP), OpenSecrets.org, Wikileaks, the US Government Open Data Initiative and the Internal Revenue Service (IRS).

This is a non-exhaustive list that do no mention a certain numbers of public datasources for which I have built scrappers.

#### Objectives and roadmap:

The objectives of this project are to process, aggregate and centralize large amounts of data relating to US politics and the blur line separating public and private interest. Graph database such as Neo4j offer a data model that suits the real-world toppology of our object of study. It is of course possible to run queries against the database and attempt to extract interesting or unusual patterns (e.g cycles or paths). This could be used to demonstrate potential conflicts of interests for example. I plan to offer an hosted version of the graph with a graph visualisation tool. Contact me if you are interested in sponsoring this project.

Moreover, this project is also ran as an experiment to validate or refute the following hypothesis: Is the traditional nomenclature that oppose Republicans to Democrats (and vice-versa) truly relevant? Or is it possible to clusterize politicians in factions that would better showcase the power dynamics at play in Congress? This is what we will try to figure out, "crunching" data about funding networks, voting history, (co-)sponsored bills and try to assess how much influence do lobbying agencies have over US politicians.

Later stage of this project will involve lots of data analysis that will be used to increase the depth and quality of our semantic network. For example, it could be interesting to use the Stanford CoreNLP library to classify the stances that lobbying agencies take with respect to certain bills or amendments. Even more so if we can simultaneously observe if a politician X who has been helped by a corporation Y through a 527 committee Z will conform to the desire of a lobbying agency A hired by the same company Y. And how frequently does this happen?

### Short overview:

Once a dataset has been scrapped or downloaded, it must be preprocessed and aggregated to an already existing "object" (e.g aggregating financial data about a legislator's latest campaign expenditures). Following this cleaning-aggregation step, we generate a CSV file that will be later fed to the graph-db uploader.

### Datasets:

When the parsers/transformers are running, the raw datasets should be available in the datasets/raw/ directory. You will notice that the current data/raw_data directory is empty. This is because Github has an upper bound (100Mb) on the filesize one can upload to a repository. You can find the raw datasets [here](http://fs.rely.io/public/32104/eazrae/data.tar.gz)

### Disclaimer:

This is a toy-project I have started because I have an interest in graph databases, information retrieval and semantic networks. I will do my best-effort to accomodate reasonable feature requests but I provide no guarantees of execution.

### Directory structure

 - datasets/raw/: Raw datasets

 - datasets/preprocessed/: Cleaned and aggregated datasets

 - datasets/processed/: CSV-JSON files that are ready for import

 - src/extract_aggreg/: Preprocessing tools

 - src/transform/: Processing tools

 - src/load/: Bulk-writing and import tools for the db.

 - src/graph-alg/: Fraud detection and Cipher queries running on top of Neo4j

 - config/: Configuration files/scripts


#### Early-stage examples:
![Congress](https://i.imgur.com/UI7Jeiy.png "An excerpt of a graph representing basic connections between congressmen and their political parties and office")
![CongressAndLobbying](https://i.imgur.com/V3b5zYY.png "Congressmen, lobbyists and parties")
![Lobbying](https://i.imgur.com/vzWIZZC.jpg "Lobbying agencies and their employees")


#### Some metrics:

Number of vertices (nodes) in our graph as of October 8th. 2016

 - MATCH (n) RETURN COUNT(n): 3,314,779 nodes
 
Number of edges (relationships) in our graph as of October 8th. 2016:

- MATCH ()-[r]-() RETURN COUNT(r): 4,608,010 relationships


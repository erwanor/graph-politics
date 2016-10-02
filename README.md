# graph-politics

Gather and organize semantics relationships about politicians, lobbyists, companies, organisations, journalists and their financial assets from publicly available sources. This includes the FEC (Federal Election Commission, USG Open Data Initiative, Wikileaks and miscelleaneous scrapping and information extraction from news articles).

Once it is scrapped, parsed and processed this data is uploaded to a Neo4j graph database against which we can run a fraud detection algorithms (looking for conflicts of interests i.e specific cycles in our graph for example) or double check if the current political nomenclature is any relevant.

Yes, congressmen are affiliated to parties and in theory they share a common set of ideological beliefs. However, using their respective voting history and network of funding supporters (lobbyists, PACs, interests groups etc.) it should be possible to extract patterns and see if party labels are still any relevant. Indeed since funding is a key element for most politician it may be that the US political landscape is actually fragmented along lines that delimited by which company/IG is supporting said politicians. The idea is to make political factions and power struggles that are unknown appear in clear sight.

This is a toy project that I have started to fulfill my interest in graph database and semantic networks. It is published under an MIT licence and might interest data journalists or concerned citizens. I will provide a web interface and a hosted version of the final graph database so anyone can run queries and maybe uncover some interesting patterns. 

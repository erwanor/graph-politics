USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///lobbyists_data.csv" AS row FIELDTERMINATOR '%'
MATCH (n:Lobbyist { CUID: row.CUID_lobbyist }), (m:Lobbying_Firm { CUID: row.CUID_employer })
    CREATE (n)-[:WORKS_FOR]->(m);

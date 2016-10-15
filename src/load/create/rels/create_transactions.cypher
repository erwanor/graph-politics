//Import lobbyists
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///lobbying_transactions.csv" AS row FIELDTERMINATOR '%'
MATCH (n:Corporation { CUID: row.CUID_corp }), (m:Lobbying_Firm { CUID: row.CUID_lobby })
    CREATE (m)-[:WORKS_FOR]->(n), CREATE (n)-[:HIRED { amount_paid: row.amount_paid }]->(m);

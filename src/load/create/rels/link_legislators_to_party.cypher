USING PERIODIC COMMIT
LOAD CSV FROM HEADERS "file://legislators.csv" AS row FIELDTERMINATOR '%'
    MATCH (n:Legislator { CUID: row.CUID_legislator }), (m:Party { name: row.party })
        CREATE (n)-[:MEMBER_OF]-(m);

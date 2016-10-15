//Import lobbyists
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///lobbyists_data.csv" AS row FIELDTERMINATOR '%'
CREATE (:Lobbyist {
    full_name: row.lobbyist_name,
    CUID: row.CUID_lobbyist,
    date: row.year });

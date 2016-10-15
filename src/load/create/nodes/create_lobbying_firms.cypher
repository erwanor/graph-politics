//Import lobbying firms
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///lobbying_firms.csv" AS row FIELDTERMINATOR '%'
CREATE (:Lobbying_Firm {
    firm_name: row.lobby_name,
    CUID: row.CUID_lobby });

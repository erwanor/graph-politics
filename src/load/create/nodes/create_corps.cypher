USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file://lobbying_client_corporations.csv" AS row FIELDTERMINATOR '%'
CREATE (:Corporation {
    name: row.corp_name,
    CUID: row.CUID_corp });

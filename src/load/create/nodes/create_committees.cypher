//Import congressional committees
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///congressional_committees_current.csv" AS row FIELDTERMINATOR '%'
CREATE (:Committee {
    committee_name: row.name,
    CUID: row.CUID,
    chamber: row.chamber });

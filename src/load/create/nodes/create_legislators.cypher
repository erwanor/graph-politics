// Import legislators - congresspeople
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///current_legislators.csv" AS row FIELDTERMINATOR '%'
CREATE (:Legislator:Congressperson {
    full_name: row.full_name,
    CUID: row.CUID,
    chamber: row.chamber,
    party: row.party,
    dob: row.dob,
    state: row.state });

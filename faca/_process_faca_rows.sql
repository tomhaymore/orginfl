# Note! This script should be executed after loading data from CSV file

# Match and link individuals between the tables for each new raw faca table
UPDATE raw_faca JOIN indivs as i
	ON raw_faca.indiv_id IS NULL AND i.last = raw_faca.lastname AND i.first = raw_faca.firstname AND i.middle = raw_faca.middlename
SET raw_faca.indiv_id = i.id;
SHOW WARNINGS;

# Insert individuals with no match from above script
SET @currentTs = CURRENT_TIMESTAMP;
INSERT IGNORE INTO indivs
    (name, last, first, middle, prefix, suffix, created)
SELECT
    CONCAT(prefix," ", lastname ,", ",firstname," ",middlename," ",suffix), lastname, firstname, middlename, prefix, suffix, @currentTs
FROM raw_faca
WHERE indiv_id IS NULL;
SHOW WARNINGS;

# For new entries, set raw faca indiv id for affs
UPDATE raw_faca JOIN indivs as i
	ON raw_faca.indiv_id IS NULL AND i.last = raw_faca.lastname AND i.first = raw_faca.firstname AND i.middle = raw_faca.middlename
SET raw_faca.indiv_id = i.id
WHERE raw_faca.indiv_id IS NULL;
SHOW WARNINGS;

# Match and link organizations to the raw_faca_matching table for each new raw faca table
UPDATE raw_faca JOIN raw_faca_match AS rfm
    ON raw_faca.org_id IS NULL AND rfm.data = raw_faca.occupationoraffiliation
SET raw_faca.org_id = rfm.id;
SHOW WARNINGS;

CREATE INDEX raw_faca_org_id_idx ON raw_faca (org_id);
CREATE INDEX raw_faca_agencyabbr_idx ON raw_faca(agencyabbr);
CREATE INDEX raw_faca_committeename_idx ON raw_faca(committeename);

# Match and link committees from raw faca
UPDATE raw_faca JOIN committees AS c
	ON raw_faca.comm_org_id IS NULL AND c.name = raw_faca.committeename
SET raw_faca.comm_org_id = c.id;
SHOW WARNINGS;

# Insert new committees into database
SET @currentTs = CURRENT_TIMESTAMP();
INSERT IGNORE INTO committees
	(name, agencyabbr, created)
SELECT DISTINCT
	committeename, agencyabbr, @currentTs
FROM raw_faca
WHERE raw_faca.comm_org_id IS NULL;
SHOW WARNINGS;

# Match and link the newly inserted committees from raw faca
UPDATE raw_faca JOIN committees AS c
	ON raw_faca.comm_org_id IS NULL AND c.name = raw_faca.committeename
SET raw_faca.comm_org_id = c.id
WHERE raw_faca.comm_org_id IS NULL;
SHOW WARNINGS;

# Update committee agency ID for new entries
UPDATE committees as c
JOIN agencies as a ON c.agencyabbr = a.abbr
SET c.agency_ID = a.id
WHERE c.agency_id IS NULL;

# Make sure same indiv committe affiliation doesn't get put twice
UPDATE affs as a
JOIN raw_faca as rf ON a.e1_id = rf.indiv_id AND a.e1_type = 'indiv' AND a.e2_id = rf.comm_org_id AND a.e2_type = 'committee'
SET rf.comm_added = 1;

# Update table for timeline so there are no repeats for individuals
UPDATE affs as a
JOIN raw_faca as rf ON a.e1_id = rf.indiv_id AND a.e1_type = 'indiv' AND a.e2_id = rf.comm_org_id AND a.e2_type = 'committee'
SET a.start = IF(rf.startdate < a.start,rf.startdate,a.start),
a.end = IF(rf.enddate > a.end, rf.enddate, a.end)
WHERE rf.indiv_id IS NOT NULL AND rf.comm_org_id IS NOT NULL;

CREATE INDEX raw_faca_affs_idx ON raw_faca (agency_org_id, org_id);
ALTER TABLE affs DISABLE KEYS;
SET @currentTs = CURRENT_TIMESTAMP();

# Match affiliation between individual and committee
INSERT IGNORE INTO affs
    (type, e1_id, e1_type, e2_id, e2_type, 
    start, end, faca_appt_type,
    faca_appt_term, faca_pay_plan, faca_pay_src, created,
    descr1
    )
SELECT 
    'advisory,faca',
    r.indiv_id,
    'indiv',
    r.comm_org_id, 
    'committee', 
    r.startdate, 
    r.enddate, 
    r.appointmenttype,
    r.appointmentterm,
    r.payplan,
    r.paysource,
    @currentTs, 
    'advisory committee representative'
FROM raw_faca AS r
WHERE r.indiv_id  IS NOT NULL AND r.comm_org_id IS NOT NULL AND r.comm_added IS NULL;
SHOW WARNINGS;

ALTER TABLE raw_faca DROP INDEX raw_faca_affs_idx;

/* Normalize Chairperson */
UPDATE affs as a
JOIN raw_faca as rf ON a.e1_id = rf.indiv_id AND a.e2_id = rf.comm_org_id AND a.e2_type = 'committee'
SET a.faca_is_chair = 1
WHERE rf.chairperson like "%yes%" OR rf.chairperson like "Cha";

UPDATE affs as a
SET faca_is_chair = 0
WHERE faca_is_chair IS NULL;

/* Normalizing Appointment Type */
UPDATE affs as a
SET faca_appt_type = "Not Applicable"
WHERE faca_appt_type = "n/a" OR faca_appt_type = "" OR faca_appt_type = "Not Reported";

/* Normalizing Appointment Term */
UPDATE affs as a
SET faca_appt_term = "Not Applicable"
WHERE faca_appt_term = "n/a" OR faca_appt_term = "" OR faca_appt_term = "Not Reported";

/* Normalizing Pay Plan */
UPDATE affs as a
SET faca_pay_plan = "Not Applicable"
WHERE faca_pay_plan = "n/a" OR faca_pay_plan = "" OR faca_pay_plan = "Not Reported"
OR faca_pay_plan = "N/A";

UPDATE affs as a
SET faca_pay_plan = "None"
WHERE faca_pay_plan like "%None%" OR faca_pay_plan = "Npne";

/* Normalizing Pay Source*/
UPDATE affs as a
SET faca_pay_src = "Not Applicable"
WHERE faca_pay_src = "n/a" OR faca_pay_src = "Not Reported" OR faca_pay_src = "" ;

UPDATE affs as a
SET faca_pay_src = "Executive Branch"
WHERE faca_pay_src = "Executive" OR faca_pay_src = "Exeuctive Branch";

# Make sure same individual/organization affiliation is not added twice
UPDATE raw_faca as rf
JOIN affs as a ON a.e1_id = rf.indiv_id AND a.e1_type = 'indiv' AND a.e2_id = rf.org_id AND a.e2_type = 'org'
SET rf.org_added = 1;

# Match affiliation between individual and company
INSERT IGNORE INTO affs
    (type, e1_id, e1_type, e2_id, e2_type, 
    start, end, created)
SELECT 
    'employment',
    r.indiv_id, 
    'indiv', 
    r.org_id,
    'org',
    NULL,
    NULL,
    @currentTs
FROM raw_faca AS r
WHERE r.indiv_id  IS NOT NULL AND r.org_id IS NOT NULL AND r.org_added is NULL;
SHOW WARNINGS;

ALTER TABLE raw_faca DROP INDEX raw_faca_org_id_idx;
ALTER TABLE raw_faca DROP INDEX raw_faca_agencyabbr_idx;
ALTER TABLE raw_faca DROP INDEX raw_faca_committeename_idx;

ALTER TABLE affs ENABLE KEYS;
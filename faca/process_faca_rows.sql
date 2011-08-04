-- NB! This script should be executed after loading data from CSV file

-- Match and link individuals
UPDATE raw_faca JOIN indivs as i
	ON raw_faca.indiv_id IS NULL AND i.last = raw_faca.lastname AND i.first = raw_faca.firstname AND i.middle = raw_faca.middlename
SET raw_faca.indiv_id = i.id

-- Insert individuals with no match
SET @currentTs = CURRENT_TIMESTAMP();
INSERT IGNORE INTO indivs
    (`name`, `last`, `first`, middle, `prefix`, suffix, created )
SELECT 
    CONCAT(`prefix`," ",lastname,", ",firstname," ",middlename," ",suffix), lastname, firstname, middlename, prefix, suffix, @currentTs
FROM raw_contracts
WHERE indiv_id IS NULL;

-- Match and link individuals
UPDATE raw_faca JOIN indivs as i
	ON raw_faca.indiv_id IS NULL AND i.last = raw_faca.lastname AND i.first = raw_faca.firstname AND i.middle = raw_faca.middlename
SET raw_faca.indiv_id = i.id

-- Match and link organizations to the raw_faca_matching table.
UPDATE raw_faca JOIN raw_faca_match AS rf
    ON raw_faca.org_id IS NULL AND rf.data = raw_faca.occupationoraffiliation
SET raw_faca.org_id = rf.id;

CREATE INDEX raw_faca_org_id_idx ON raw_faca (org_id);

-- Match and link agencies
CREATE INDEX raw_faca_agencyabbr_idx ON raw_faca(agencyabbr);

-- ALTER TABLE raw_faca DISABLE KEYS;

UPDATE raw_faca JOIN orgs_agencies AS oa
    ON raw_faca.agencyabbr=oa.org_agency_abbr
SET raw_faca.agency_org_id = oa.org_id;

-- ALTER TABLE raw_faca ENABLE KEYS;

-- Match and link committees

CREATE INDEX raw_faca_committeename_idx ON raw_faca(committeename);

UPDATE raw_faca JOIN orgs AS o
	ON raw_faca.comm_org_id IS NULL AND o.name = raw_faca.committeename
SET raw_faca.comm_org_id = o.id

-- insert new committees

SET @currentTs = CURRENT_TIMESTAMP();
INSERT IGNORE INTO orgs
	(`name`,`type`,`parent`,`created`)
SELECT DISTINCT
	committeename, 'Org,GovernmentEntity,AdvisoryCommittee', agency_org_id, @currentTs
FROM raw_faca
WHERE raw_faca.comm_org_id IS NULL

-- match new committees

UPDATE raw_faca JOIN orgs AS o
	ON raw_faca.comm_org_id IS NULL AND o.name = raw_faca.committeename
SET raw_faca.comm_org_id = o.id

-- Process Affiliations:
SET @lastAffId=IFNULL( (SELECT MAX(id) FROM affs), 0);
SELECT @lastAffId AS `Last Aff Id`;

-- between individual and committee
CREATE INDEX raw_faca_affs_idx ON raw_faca (agency_org_id, org_id);
ALTER TABLE affs DISABLE KEYS;
SET @currentTs = CURRENT_TIMESTAMP();

INSERT IGNORE INTO affs
    (`type`, e1_id, e1_type, e2_id, e2_type, 
    `start`, `end`, `created`,
    descr1
    )
SELECT 
    'advisory,faca',
    indiv_id,
    'indiv', comm_id, 
    'org', 
    effectivedate, 
    ultimatecompletiondate, 
    @currentTs, 
	'advisory committee representative'

FROM raw_faca AS r
WHERE indiv_id  IS NOT NULL AND comm_id IS NOT NULL;

ALTER TABLE raw_faca DROP INDEX raw_faca_affs_idx;

-- between individual and company

INSERT IGNORE INTO affs
    (`type`, e1_id, e1_type, e2_id, e2_type, 
    `start`, `end`, `created`)
SELECT 
    'employment',
    org_id,
    'org', indiv_id, 
    'indiv', 
    --, 
    --, 
    @currentTs
FROM raw_faca AS r
WHERE indiv_id  IS NOT NULL AND org_id IS NOT NULL;

ALTER TABLE raw_faca DROP INDEX raw_faca_affs_idx;

ALTER TABLE affs ENABLE KEYS;


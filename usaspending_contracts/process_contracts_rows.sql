-- NB! This script should be executed after loading data from CSV file

SET @lastOrgId=IFNULL( (SELECT MAX(id) AS last_org_id FROM orgs), 0);
SELECT @lastOrgId AS `Last Org Id`;

-- ALTER TABLE raw_row DROP INDEX raw_row_org_id_idx;

-- Normalize Names:
UPDATE raw_row
SET vendorname=normal_name(vendorname),
    vendoralternatename=normal_name(vendoralternatename),
    vendorlegalorganizationname=normal_name(vendorlegalorganizationname),
    vendordoingasbusinessname=normal_name(vendordoingasbusinessname);

-- Match and link organizations to the loaded raw data.
UPDATE raw_row JOIN orgs AS o
    ON raw_row.org_id IS NULL AND o.name = raw_row.vendorname
SET raw_row.org_id = o.id;
UPDATE raw_row JOIN orgs_aliases AS a
    ON raw_row.org_id IS NULL AND a.`name` = raw_row.vendorname
SET raw_row.org_id = a.org_id;

-- Create Orgs if no match found
SET @currentTs = CURRENT_TIMESTAMP();
INSERT IGNORE INTO orgs
    (`name`, `type`, created )
SELECT -- DISTINCT -- TODO: check if it can improve performance
    vendorname, 'GovernmentContractor', @currentTs
FROM raw_row
WHERE org_id IS NULL;

-- Match rows to the new orgs:
UPDATE raw_row JOIN orgs AS o
    ON raw_row.org_id IS NULL AND o.name = raw_row.vendorname
SET raw_row.org_id = o.id;

CREATE INDEX raw_row_org_id_idx ON raw_row (org_id);


-- Insert or update org meta data:
INSERT INTO orgs_fin
    (org_id, fiscal_year, employees, revenue)
SELECT
    org_id, fiscal_year, numberofemployees, annualrevenue
FROM raw_row
WHERE org_id IS NOT NULL
ON DUPLICATE KEY UPDATE
    fiscal_year = fiscal_year
    employees = numberofemployees,
    revenue = annualrevenue,

-- Insert org contact data:
INSERT IGNORE INTO orgs_contacts (
    org_id, address1, address2, address3,
    city, `state`, zip, country,cd, phone, fax
)
SELECT
    org_id, streetaddress, streetaddress2,
    streetaddress3,city,`state`,zipcode,
    vendorcountrycode,vendor_cd, phoneno, faxno
FROM raw_row
WHERE org_id IS NOT NULL;

/*
INSERT IGNORE INTO orgs_ext
    (org_ext_local_id, org_ext_local_type, org_ext_remote_src)
SELECT
    org_id, 'org', 'usaspending'
FROM orgs
WHERE org_id>@lastOrgId;
*/

-- Process only aliases of new organizations:
INSERT IGNORE INTO orgs_aliases ( org_id, `name`)
SELECT org_id, vendoralternatename
FROM raw_row WHERE vendoralternatename IS NOT NULL AND org_id IS NOT NULL
    AND org_id > @lastOrgId
UNION -- ALL
SELECT org_id, vendorlegalorganizationname
FROM raw_row WHERE vendorlegalorganizationname IS NOT NULL AND org_id IS NOT NULL
    AND org_id > @lastOrgId
UNION -- ALL
SELECT org_id, vendordoingasbusinessname
FROM raw_row WHERE vendordoingasbusinessname IS NOT NULL AND org_id IS NOT NULL
    AND org_id >@lastOrgId;

-- Process DUNS:
INSERT IGNORE orgs_refs ( org_id, duns)
SELECT org_id, dunsnumber FROM raw_row
WHERE org_id IS NOT NULL AND dunsnumber IS NOT NULL AND dunsnumber!=''
UNION
SELECT org_id, parentdunsnumber FROM raw_row
WHERE org_id IS NOT NULL AND parentdunsnumber IS NOT NULL AND parentdunsnumber!='';

-- Match and link agencies
CREATE INDEX raw_row_maj_agency_cat_idx ON raw_row( maj_agency_cat);

-- ALTER TABLE raw_row DISABLE KEYS;
UPDATE raw_row JOIN orgs_agencies AS oa
    ON raw_row.maj_agency_cat=oa.org_agency_code
SET raw_row.agency_org_id = oa.org_agency_o_id;
-- ALTER TABLE raw_row ENABLE KEYS;

-- Create agnency orgs if no match found
SET @lastAgencyOrgId = (SELECT MAX(id) FROM orgs);
SELECT @lastAgencyOrgId AS `Last Agency Org Id`;

SET @currentTs = CURRENT_TIMESTAMP();
INSERT IGNORE INTO orgs
    ( `name`, agency_code, `type`, org_created )
SELECT 
    CONCAT('U.S. ', TRIM(SUBSTRING_INDEX( `name`,':',-1)) ) AS org_name,
    a.org_name, NULL, 'GovernmentEntity,Federal,Agency', @currentTs
FROM
( SELECT DISTINCT
    maj_agency_cat AS org_name
FROM raw_row
WHERE agency_org_id IS NULL ) AS a;

/*
UPDATE orgs SET org_name_length = LENGTH( org_name)
WHERE org_id>@lastAgencyOrgId;
*/

CREATE INDEX orgs_org_agency_code_idx ON orgs(org_agency_code);

INSERT IGNORE INTO orgs_agencies ( code, org_id)
SELECT DISTINCT agency_code, id
FROM orgs
WHERE id>@lastAgencyOrgId;

ALTER TABLE orgs DROP INDEX orgs_org_agency_code_idx;

UPDATE orgs
SET is_govt = 1, is_fed = 1
WHERE id > @lastAgencyOrgId;

/*
INSERT IGNORE INTO orgs_ext
    ( org_ext_local_type, org_ext_local_id, org_ext_remote_src)
SELECT 'org', org_id, 'usaspending'
FROM orgs
WHERE org_id>@lastAgencyOrgId;
*/

-- Match and link missing agencies:
CREATE INDEX raw_row_agency_org_id_idx ON raw_row( agency_org_id);
UPDATE raw_row JOIN orgs_agencies AS oa
    ON  raw_row.maj_agency_cat IS NOT NULL 
        AND oa.code=raw_row.maj_agency_cat
        AND raw_row.agency_org_id IS NULL
SET raw_row.agency_org_id = oa.org_id;

-- Process Affiliations:
SET @lastAffId=IFNULL( (SELECT MAX(id) FROM affs), 0);
SELECT @lastAffId AS `Last Aff Id`;


CREATE INDEX raw_row_affs_idx ON raw_row (agency_org_id, org_id);
ALTER TABLE affs DISABLE KEYS;
SET @currentTs = CURRENT_TIMESTAMP();

INSERT IGNORE INTO affs
    (`type`, e1_id, e1_type, e2_id, e2_type, 
    `start`, `end`, `created`, trans_id,
    descr1, 
    descr2, 
    amount, 
    trans_descr1, 
    trans_descr2)
SELECT 
    'contract,transaction,governmentContract',
    agency_org_id,
    'org', org_id, 
    'org', 
    effectivedate, 
    ultimatecompletiondate, 
    @currentTs, 
    unique_transaction_id,
    r.descriptionofcontractrequirement,
    r.obligatedamount,
    r.psc_cat,
    r.productorservicecode
FROM raw_row AS r
WHERE agency_org_id  IS NOT NULL AND org_id IS NOT NULL;

ALTER TABLE raw_row DROP INDEX raw_row_affs_idx;

ALTER TABLE affs ENABLE KEYS;

/*
ALTER TABLE affs_meta DISABLE KEYS;

INSERT IGNORE INTO affs_meta
    ( aff_meta_aff_id, 
    aff_meta_subtype, 
    aff_meta_descr1, 
    aff_meta_descr2, 
    aff_meta_amount, 
    aff_meta_trans_descr1, 
    aff_meta_trans_descr2)
SELECT
    a.aff_id,
    'transaction,governmentContract',
    HEX(r.unique_transaction_id), 
    r.descriptionofcontractrequirement,
    r.obligatedamount, r.psc_cat, r.productorservicecode
FROM affs AS a JOIN raw_row AS r 
    ON a.aff_id > @lastAffId AND r.unique_transaction_id = a.unique_transaction_id;

ALTER TABLE affs_meta ENABLE KEYS;*/

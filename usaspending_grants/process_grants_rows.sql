-- NB! This script should be executed after loading data from CSV file

SET @lastOrgId=IFNULL( (SELECT MAX(id) AS last_org_id FROM orgs), 0);
SELECT @lastOrgId AS `Last Org Id`;

-- ALTER TABLE raw_grants DROP INDEX raw_grants_org_id_idx;

-- Normalize Names:
UPDATE raw_grants
SET vendorname=normal_name(vendorname),
    vendoralternatename=normal_name(vendoralternatename),
    vendorlegalorganizationname=normal_name(vendorlegalorganizationname),
    vendordoingasbusinessname=normal_name(vendordoingasbusinessname);

-- Match and link organizations to the loaded raw data.
UPDATE raw_grants JOIN orgs AS o
    ON raw_grants.org_id IS NULL AND o.name = raw_grants.recipientname
SET raw_grants.org_id = o.id;

-- no aliases for grants db
/*
UPDATE raw_grants JOIN orgs_aliases AS a
    ON raw_grants.org_id IS NULL AND a.`name` = raw_grants.vendorname
SET raw_grants.org_id = a.org_id;
*/

-- Create Orgs if no match found
SET @currentTs = CURRENT_TIMESTAMP();
INSERT IGNORE INTO orgs
    (`name`, `type`, created )
SELECT -- DISTINCT -- TODO: check if it can improve performance
    recipientname, CONCAT('GovernmentFundsRecipient',recipient_type), @currentTs
FROM raw_grants
WHERE org_id IS NULL;

-- Match rows to the new orgs:
UPDATE raw_grants JOIN orgs AS o
    ON raw_grants.org_id IS NULL AND o.name = raw_grants.recipientname
SET raw_grants.org_id = o.id;

CREATE INDEX raw_grants_org_id_idx ON raw_grants (org_id);

-- Insert org contact data:
INSERT IGNORE INTO orgs_contacts (
    org_id, address1, address2, address3, city, zip
)
SELECT
    org_id, receip_addr1, receip_addr2, receip_addr3, recipient_city_name, recipient_zip
FROM raw_grants
WHERE org_id IS NOT NULL;

/*
INSERT IGNORE INTO orgs_ext
    (org_ext_local_id, org_ext_local_type, org_ext_remote_src)
SELECT
    org_id, 'org', 'usaspending'
FROM orgs
WHERE org_id>@lastOrgId;
*/

-- Process DUNS:
INSERT IGNORE orgs_refs ( org_id, duns)
SELECT org_id, duns_no FROM raw_grants
WHERE org_id IS NOT NULL AND duns_no IS NOT NULL AND duns_no !=''

-- Match and link agencies
CREATE INDEX raw_grants_maj_agency_cat_idx ON raw_grants( maj_agency_cat);

-- ALTER TABLE raw_grants DISABLE KEYS;
UPDATE raw_grants JOIN orgs_agencies AS oa
    ON raw_grants.maj_agency_cat=oa.org_agency_code
SET raw_grants.agency_org_id = oa.org_agency_o_id;
-- ALTER TABLE raw_grants ENABLE KEYS;

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
FROM raw_grants
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
CREATE INDEX raw_grants_agency_org_id_idx ON raw_grants( agency_org_id);
UPDATE raw_grants JOIN orgs_agencies AS oa
    ON  raw_grants.maj_agency_cat IS NOT NULL 
        AND oa.code=raw_grants.maj_agency_cat
        AND raw_grants.agency_org_id IS NULL
SET raw_grants.agency_org_id = oa.org_id;

-- Process Affiliations:
SET @lastAffId=IFNULL( (SELECT MAX(id) FROM affs), 0);
SELECT @lastAffId AS `Last Aff Id`;


CREATE INDEX raw_grants_affs_idx ON raw_grants (agency_org_id, org_id);
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
    'grant,transaction,governmentGrant',
    agency_org_id,
    'org', org_id, 
    'org', 
    starting_date, 
    ending_date, 
    @currentTs, 
    unique_transaction_id,
    project_description,
    account_title,
    fed_funding_amount,
    action_type,
    assistance_type
FROM raw_grants AS r
WHERE agency_org_id  IS NOT NULL AND org_id IS NOT NULL;

ALTER TABLE raw_grants DROP INDEX raw_grants_affs_idx;

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
FROM affs AS a JOIN raw_grants AS r 
    ON a.aff_id > @lastAffId AND r.unique_transaction_id = a.unique_transaction_id;

ALTER TABLE affs_meta ENABLE KEYS;*/

-- Alternations in DB model:
-- check to make sure that this matches up with new database structure

USE orginfl;

DROP FUNCTION IF EXISTS normal_name;

DELIMITER $$
CREATE FUNCTION normal_name (v TEXT)
RETURNS TEXT
    COMMENT 'Normalize a string stripping delimiters and excluding delimiter repeats'
    LANGUAGE SQL
    DETERMINISTIC
    CONTAINS SQL
BEGIN
SET v = TRIM(
REPLACE( REPLACE(v,'\t',' '), '  ', ' '));
IF v='' THEN SET v=NULL; END IF;
RETURN v;
END$$

DELIMITER ;

ALTER TABLE orgs DROP INDEX org_name;
ALTER IGNORE TABLE orgs ADD UNIQUE INDEX org_name_UNIQUE (org_name(333) ASC);

ALTER IGNORE TABLE orgs_meta
ADD UNIQUE INDEX org_meta_org_id_UNIQUE (org_meta_org_id ASC);

ALTER TABLE orgs_contact 
CHANGE COLUMN org_contact_id org_contact_id BIGINT NOT NULL AUTO_INCREMENT;
ALTER TABLE orgs_contact 
CHANGE COLUMN org_contact_org_id org_contact_org_id BIGINT NULL DEFAULT NULL;

ALTER IGNORE TABLE orgs_contact 
ADD UNIQUE INDEX org_contact_org_id_UNIQUE (org_contact_org_id ASC);

-- ALTER TABLE orgs_contact DROP INDEX org_contact_UNIQUE;
ALTER IGNORE TABLE orgs_contact
ADD UNIQUE INDEX org_contact_UNIQUE
(
    org_contact_org_id,
    org_contact_address1 (100), org_contact_address2(100), org_contact_address3(100), 
    org_contact_city, org_contact_state, org_contact_zip, org_contact_country, org_contact_cd, 
    org_contact_phone, org_contact_fax
);

ALTER IGNORE TABLE orgs_ext 
ADD UNIQUE INDEX org_ext_local_id_UNIQUE (org_ext_local_id);

DROP TABLE IF EXISTS org_ref_duns;
CREATE TABLE IF NOT EXISTS  org_ref_duns (
  org_ref_duns_id BIGINT NOT NULL AUTO_INCREMENT,
  org_id BIGINT NOT NULL,
  duns VARCHAR(50) NOT NULL,
  PRIMARY KEY (org_ref_duns_id),
  UNIQUE INDEX org_ref_duns_UNIQUE (org_id ASC, duns ASC) );

ALTER IGNORE TABLE affs
ADD unique_transaction_id BINARY(16);

-- ALTER TABLE affs_meta DROP INDEX aff_meta_aff_id_UNIQUE;
ALTER IGNORE TABLE affs_meta 
ADD UNIQUE INDEX aff_meta_aff_id_UNIQUE (aff_meta_aff_id ASC);

ALTER TABLE orgs ADD org_agency_code varchar(100) NULL;

ALTER IGNORE TABLE affs DROP INDEX affs_unique_transaction_id_UNIQUE;

ALTER IGNORE TABLE affs ADD UNIQUE INDEX aff_UNIQUE (unique_transaction_id, aff_e1_id, aff_e2_id);

ALTER IGNORE TABLE affs_meta DROP INDEX aff_meta_aff_id;

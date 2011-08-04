-- USE cdrg;

DROP TABLE IF EXISTS raw_grants;

CREATE TABLE raw_grants (
	unique_transaction_id  BINARY(16) /*PRIMARY KEY*/, -- Field 0
	account_title VARCHAR(450),
	recipient_name VARCHAR(450),
	recipient_city_name VARCHAR(450),
	recipient_county_name VARCHAR(150),
	recipient_zip INT(9),
	recipient_type VARCHAR(150),
	action_type VARCHAR(150),
	agency_code VARCHAR(150),
	federal_award_id VARCHAR(45),
	fed_funding_amount DECIMAL(25,2),
	non_fed_funding_amount DECIMAL(25,2),
	total_funding_amount DECIMAL(25,2),
	starting_date DATE,
	ending_date DATE,
	assistance_type VARCHAR(150),
	principal_place_state VARCHAR(150),
	principal_place_cc VARCHAR(150),
	principal_place_zip INT(9),
	principal_place_cd VARCHAR(4),
	cfda_program_title VARCHAR(150),
	agency_name VARCHAR(15),
	project_description VARCHAR(150),
	duns_no VARCHAR(15),
	progsrc_agen_code INT(2),
	receip_addr1 VARCHAR(150),
	receip_addr2 VARCHAR(150),
	receip_addr3 VARCHAR(150),
	fiscal_year YEAR,
	recip_cat_type VARCHAR(150),
	asst_cat_type VARCHAR(150),
	recipient_cd VARCHAR(150),
	maj_agency_cat VARCHAR(150),
	uri VARCHAR(250),
	org_id BIGINT NULL,
	agency_org_id BIGINT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
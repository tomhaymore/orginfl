-- USE orginfl;

DROP TABLE IF EXISTS raw_faca;

CREATE TABLE raw_faca (
	agencyabbr VARCHAR(15),
	committeename VARCHAR(450),
	cno INT(10),
	fy YEAR,
	`prefix` VARCHAR(45),
	firstname VARCHAR(450),
	middlename VARCHAR(450),
	lastname VARCHAR(450),
	suffix VARCHAR(45),
	memberdesignation VARCHAR(150),
	representedgroup VARCHAR(150),
	chairperson VARCHAR(4),
	occupationoraffiliation VARCHAR(450),
	startdate DATETIME,
	enddate DATETIME,
	appointmenttype VARCHAR(150),
	appointmentterm VARCHAR(15),
	payplan VARCHAR(150),
	paysource VARCHAR(150),
	org_id BIGINT NULL,
	comm_org_id BIGINT NULL,
  	agency_org_id BIGINT NULL,
  	indiv_id BIGINT NULL,
  	indiv_start DATE NULL,
  	indiv_end DATE NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

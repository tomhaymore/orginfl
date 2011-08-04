# Sequel Pro dump
# Version 2492
# http://code.google.com/p/sequel-pro
#
# Host: localhost (MySQL 5.5.11)
# Database: cdrg
# Generation Time: 2011-05-10 08:51:40 -0700
# ************************************************************

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table affs
# ------------------------------------------------------------

DROP TABLE IF EXISTS `affs`;

CREATE TABLE `affs` (
  `aff_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `aff_subtype` varchar(45) NOT NULL,
  `aff_e1_id` bigint(20) NOT NULL,
  `aff_e1_type` varchar(45) NOT NULL,
  `aff_e2_id` bigint(20) NOT NULL,
  `aff_e2_type` varchar(45) NOT NULL,
  `aff_type_id` bigint(20) DEFAULT NULL,
  `aff_ref_src` int(4) DEFAULT NULL,
  `aff_ext_id` varchar(45) DEFAULT NULL,
  `aff_sub_id` bigint(20) DEFAULT NULL,
  `aff_start` date DEFAULT NULL,
  `aff_end` date DEFAULT NULL,
  `aff_is_current` int(1) DEFAULT NULL,
  `aff_created` datetime NOT NULL,
  `aff_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `aff_status` varchar(15) NOT NULL DEFAULT 'active',
  PRIMARY KEY (`aff_id`),
  KEY `aff_type` (`aff_subtype`),
  KEY `aff_e1_id` (`aff_e1_id`,`aff_e2_id`),
  KEY `aff_e2_id` (`aff_e2_id`)
) ENGINE=MyISAM AUTO_INCREMENT=1687908 DEFAULT CHARSET=utf8;



# Dump of table affs_meta
# ------------------------------------------------------------

DROP TABLE IF EXISTS `affs_meta`;

CREATE TABLE `affs_meta` (
  `aff_meta_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `aff_meta_aff_id` bigint(20) NOT NULL,
  `aff_meta_subtype` varchar(45) NOT NULL,
  `aff_meta_faca_descr` text,
  `aff_meta_descr1` varchar(450) DEFAULT NULL,
  `aff_meta_descr2` varchar(450) DEFAULT NULL,
  `aff_meta_bundler_id` varchar(15) DEFAULT NULL,
  `aff_meta_amount` bigint(20) DEFAULT NULL,
  `aff_meta_is_goods` int(1) DEFAULT NULL,
  `aff_meta_occ_id` int(5) DEFAULT NULL,
  `aff_meta_is_board` int(1) DEFAULT NULL,
  `aff_meta_is_executive` int(1) DEFAULT NULL,
  `aff_meta_is_employee` int(1) DEFAULT NULL,
  `aff_meta_boss_id` bigint(20) DEFAULT NULL,
  `aff_meta_compensation` int(15) DEFAULT NULL,
  `aff_meta_degree_id` varchar(150) DEFAULT NULL,
  `aff_meta_field` varchar(150) DEFAULT NULL,
  `aff_meta_is_dropout` int(1) DEFAULT NULL,
  `aff_meta_dues` varchar(15) DEFAULT NULL,
  `aff_meta_percent_stake` int(2) DEFAULT NULL,
  `aff_meta_shares` bigint(20) DEFAULT NULL,
  `aff_meta_trans_contact1` bigint(20) DEFAULT NULL,
  `aff_meta_trans_contact2` bigint(20) DEFAULT NULL,
  `aff_meta_district_id` varchar(15) DEFAULT NULL,
  `aff_meta_state` varchar(2) DEFAULT NULL,
  `aff_meta_is_lobbying` int(1) DEFAULT NULL,
  `aff_meta_trans_descr1` varchar(450) DEFAULT NULL,
  `aff_meta_trans_descr2` varchar(450) DEFAULT NULL,
  `aff_meta_is_chair` int(1) DEFAULT NULL,
  `aff_meta_appt_type` varchar(50) DEFAULT NULL,
  `aff_meta_term` varchar(50) DEFAULT NULL,
  `aff_meta_pay_plan` varchar(450) DEFAULT NULL,
  `aff_meta_pay_src` varchar(450) DEFAULT NULL,
  `aff_meta_cmo` varchar(450) DEFAULT NULL,
  `aff_meta_dfo` varchar(450) DEFAULT NULL,
  `aff_meta_is_current` int(1) DEFAULT NULL,
  `aff_meta_created` datetime DEFAULT NULL,
  `aff_meta_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `aff_meta_pop_state` varchar(15) DEFAULT NULL,
  `aff_meta_pop_country` varchar(15) DEFAULT NULL,
  `aff_meta_pop_zip` varchar(15) DEFAULT NULL,
  `aff_meta_pop_cd` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`aff_meta_id`),
  KEY `aff_meta_aff_id` (`aff_meta_aff_id`)
) ENGINE=MyISAM AUTO_INCREMENT=1687908 DEFAULT CHARSET=utf8;



# Dump of table files_processed
# ------------------------------------------------------------

DROP TABLE IF EXISTS `files_processed`;

CREATE TABLE `files_processed` (
  `file_processed_id` int(11) NOT NULL AUTO_INCREMENT,
  `file_type` varchar(15) NOT NULL,
  `file_name` varchar(150) NOT NULL,
  `file_line` int(11) DEFAULT NULL,
  `file_lines_processed` int(11) DEFAULT NULL,
  `file_lines_skipped` int(11) DEFAULT NULL,
  `file_ratio_processed` float DEFAULT NULL,
  `file_status` varchar(45) NOT NULL,
  `file_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`file_processed_id`),
  KEY `file_name` (`file_name`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;


# Dump of table orgs
# ------------------------------------------------------------

DROP TABLE IF EXISTS `orgs`;

CREATE TABLE `orgs` (
  `org_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `org_name` varchar(450) NOT NULL,
  `org_name_length` int(11) NOT NULL,
  `org_abbr` varchar(15) DEFAULT NULL,
  `org_aliases` text NOT NULL,
  `org_array_match` int(1) DEFAULT '0',
  `org_array_match_list` text,
  `org_link` varchar(450) NOT NULL,
  `org_type` varchar(20) NOT NULL,
  `org_summary` text,
  `org_sub_types` varchar(150) NOT NULL,
  `org_parent_id` bigint(20) DEFAULT NULL,
  `org_created` datetime NOT NULL,
  `org_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `org_faca_id` varchar(45) DEFAULT NULL,
  `org_import_src` int(11) NOT NULL,
  `org_status` varchar(15) NOT NULL DEFAULT 'active',
  PRIMARY KEY (`org_id`),
  KEY `org_name` (`org_name`(333)),
  FULLTEXT KEY `org_aliases` (`org_aliases`)
) ENGINE=MyISAM AUTO_INCREMENT=155230 DEFAULT CHARSET=utf8;



# Dump of table orgs_agencies
# ------------------------------------------------------------

DROP TABLE IF EXISTS `orgs_agencies`;

CREATE TABLE `orgs_agencies` (
  `org_agency_id` int(11) NOT NULL AUTO_INCREMENT,
  `org_agency_code` varchar(150) DEFAULT NULL,
  `org_agency_o_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`org_agency_id`),
  KEY `org_agency_code` (`org_agency_code`),
  KEY `org_agency_o_id` (`org_agency_o_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=latin1;



# Dump of table orgs_contact
# ------------------------------------------------------------

DROP TABLE IF EXISTS `orgs_contact`;

CREATE TABLE `orgs_contact` (
  `org_contact_id` int(11) NOT NULL AUTO_INCREMENT,
  `org_contact_org_id` int(11) DEFAULT NULL,
  `org_contact_address1` varchar(450) DEFAULT NULL,
  `org_contact_address2` varchar(450) DEFAULT NULL,
  `org_contact_address3` varchar(450) DEFAULT NULL,
  `org_contact_city` varchar(150) DEFAULT NULL,
  `org_contact_state` varchar(150) DEFAULT NULL,
  `org_contact_zip` varchar(10) DEFAULT NULL,
  `org_contact_country` varchar(150) DEFAULT NULL,
  `org_contact_cd` varchar(150) DEFAULT NULL,
  `org_contact_phone` varchar(25) DEFAULT NULL,
  `org_contact_fax` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`org_contact_id`),
  KEY `org_contact_org_id` (`org_contact_org_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1784330 DEFAULT CHARSET=latin1;



# Dump of table orgs_ext
# ------------------------------------------------------------

DROP TABLE IF EXISTS `orgs_ext`;

CREATE TABLE `orgs_ext` (
  `org_ext_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `org_ext_local_type` varchar(45) DEFAULT 'org',
  `org_ext_local_id` bigint(11) DEFAULT NULL,
  `org_ext_remote_type` varchar(45) DEFAULT NULL,
  `org_ext_remote_id` int(11) DEFAULT NULL,
  `org_ext_url` varchar(450) DEFAULT NULL,
  `org_ext_added` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `org_ext_remote_src` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`org_ext_id`)
) ENGINE=MyISAM AUTO_INCREMENT=262852 DEFAULT CHARSET=utf8;



# Dump of table orgs_meta
# ------------------------------------------------------------

DROP TABLE IF EXISTS `orgs_meta`;

CREATE TABLE `orgs_meta` (
  `org_meta_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `org_meta_org_id` bigint(20) NOT NULL,
  `org_meta_rev` bigint(20) NOT NULL,
  `org_meta_rev_year` year(4) NOT NULL,
  `org_meta_employees` int(7) NOT NULL,
  `org_meta_employees_year` year(4) NOT NULL,
  `org_meta_profit` bigint(20) NOT NULL,
  `org_meta_profit_year` year(4) NOT NULL,
  `org_meta_ticker` varchar(11) NOT NULL,
  `org_meta_sec` varchar(11) NOT NULL,
  `org_meta_endowment` bigint(20) NOT NULL,
  `org_meta_endowment_year` year(4) NOT NULL,
  `org_meta_students` int(6) NOT NULL,
  `org_meta_students_year` year(4) NOT NULL,
  `org_meta_faculty` int(4) NOT NULL,
  `org_meta_faculty_year` year(4) NOT NULL,
  `org_meta_tuition` int(6) NOT NULL,
  `org_meta_tuition_year` year(4) NOT NULL,
  `org_meta_private` int(1) NOT NULL,
  `org_meta_is_govt` int(1) NOT NULL,
  `org_meta_is_fed` int(1) NOT NULL,
  `org_meta_state` varchar(45) NOT NULL,
  `org_meta_city` varchar(150) NOT NULL,
  `org_meta_county` varchar(150) NOT NULL,
  `org_meta_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `org_meta_address1` varchar(450) DEFAULT NULL,
  `org_meta_address2` varchar(450) DEFAULT NULL,
  `org_meta_address3` varchar(450) DEFAULT NULL,
  `org_meta_zip` varchar(10) DEFAULT NULL,
  `org_meta_cd` varchar(150) DEFAULT NULL,
  `org_meta_phone` varchar(25) DEFAULT NULL,
  `org_meta_fax` varchar(25) DEFAULT NULL,
  `org_meta_naics` text,
  `org_meta_revenue` varchar(150) DEFAULT NULL,
  `org_meta_revenue_year` int(4) DEFAULT NULL,
  PRIMARY KEY (`org_meta_id`),
  KEY `org_meta_org_id` (`org_meta_org_id`)
) ENGINE=MyISAM AUTO_INCREMENT=279057 DEFAULT CHARSET=utf8;



# Dump of table orgs_norms
# ------------------------------------------------------------

DROP TABLE IF EXISTS `orgs_norms`;

CREATE TABLE `orgs_norms` (
  `org_norm_id` int(11) NOT NULL AUTO_INCREMENT,
  `org_norm_pattern` varchar(150) NOT NULL,
  `org_norm_repl` varchar(150) NOT NULL,
  PRIMARY KEY (`org_norm_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=latin1;



# Dump of table orgs_ref
# ------------------------------------------------------------

DROP TABLE IF EXISTS `orgs_ref`;

CREATE TABLE `orgs_ref` (
  `org_ref_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `org_ref_org_id` bigint(20) NOT NULL,
  `org_ref_fedspending` varchar(50) NOT NULL,
  `org_ref_lda` varchar(50) NOT NULL,
  `org_ref_fec` varchar(50) NOT NULL,
  `org_ref_littlesis_id` int(15) NOT NULL,
  `org_ref_govtrack_commcode` varchar(10) NOT NULL,
  `org_ref_duns` text,
  `org_ref_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`org_ref_id`),
  KEY `org_ref_org_id` (`org_ref_org_id`)
) ENGINE=MyISAM AUTO_INCREMENT=96662 DEFAULT CHARSET=utf8;


# Dump of table subs_occ
# ------------------------------------------------------------

DROP TABLE IF EXISTS `subs_occ`;

CREATE TABLE `subs_occ` (
  `sub_occ_id` int(11) NOT NULL AUTO_INCREMENT,
  `sub_occ_name` varchar(250) NOT NULL,
  `sub_occ_reg` varchar(250) NOT NULL,
  `sub_occ_reg_python` varchar(450) NOT NULL,
  `sub_occ_length` int(11) NOT NULL,
  `sub_occ_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`sub_occ_id`)
) ENGINE=MyISAM AUTO_INCREMENT=111 DEFAULT CHARSET=utf8;



# Dump of table subs_org
# ------------------------------------------------------------

DROP TABLE IF EXISTS `subs_org`;

CREATE TABLE `subs_org` (
  `sub_org` bigint(20) NOT NULL AUTO_INCREMENT,
  `sub_org_org_id` bigint(20) NOT NULL,
  `sub_org_repl` varchar(450) NOT NULL,
  `sub_org_reg` varchar(150) NOT NULL,
  PRIMARY KEY (`sub_org`)
) ENGINE=MyISAM AUTO_INCREMENT=3620 DEFAULT CHARSET=utf8;






/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

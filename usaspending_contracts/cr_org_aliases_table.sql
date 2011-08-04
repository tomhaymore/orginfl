DROP TABLE IF EXISTS org_aliases;

CREATE TABLE IF NOT EXISTS org_aliases (
  `alias_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `org_id` bigint(20) NOT NULL,
  `name` varchar(450) NOT NULL,
  `name_length` int(11) NOT NULL,
  PRIMARY KEY (`alias_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

ALTER TABLE org_aliases DROP INDEX org_aliases_UNIQUE;

ALTER TABLE org_aliases 
ADD UNIQUE INDEX `org_aliases_UNIQUE` (`name`(330), org_id);


/* need to add more tables here */

CREATE DATABASE 'orginfl';

CREATE TABLE 'orgs' (
	id INT(11) UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(250) NOT NULL,
	types VARCHAR(150)
	) DEFAULT CHARACTER SET `utf8` ENGINE = `MyISAM`;
	
CREATE INDEX name_index ON orgs (name);

CREATE TABLE 'orgs_aliases' (
	id INT(11) UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
	org_id VARCHAR(11) NOT NULL,
	name VARCHAR(250)
	) DEFAULT CHARACTER SET 'utf8' ENGINE = 'MyISAM';

CREATE INDEX name_index on orgs_aliases (name);

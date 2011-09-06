-- USE orginfl;

DROP TABLE IF EXISTS raw_faca_match;

CREATE TABLE raw_faca_match (
	data VARCHAR(450),
	matchorg VARCHAR(450),
	id INT(10)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

ALTER TABLE raw_faca_match ENABLE KEYS;
ALTER TABLE raw_faca_match ADD INDEX raw_faca_data_idx (data);
ALTER TABLE raw_faca_match ADD INDEX raw_faca_id_idx (id);

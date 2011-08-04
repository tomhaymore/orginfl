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
REPLACE(REPLACE(REPLACE(REPLACE( REPLACE(v,'\t',' '), '  ', ' '), '  ', ' '), '  ', ' '), '  ', ' ')
);
IF v='' THEN SET v=NULL; END IF;
RETURN v;
END$$

DELIMITER ;
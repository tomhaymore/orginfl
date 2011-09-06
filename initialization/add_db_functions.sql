DROP FUNCTION IF EXISTS normal_name;
DELIMITER $$
CREATE FUNCTION normal_name (v TEXT)

RETURNS TEXT
    COMMENT 'Normalize a string stripping delimiters and excluding delimiter repeats'
    LANGUAGE SQL
    DETERMINISTIC
    CONTAINS SQL
BEGIN
	DECLARE result TEXT;
	SET result = TRIM(
	REPLACE(REPLACE(REPLACE(REPLACE( REPLACE(v,'\t',' '), '  ', ' '), '  ', ' '), '  ', ' '), '  ', ' ')
	);
	IF result='' THEN
		SET result=NULL;
		END IF;
	RETURN (result);
	SHOW WARNINGS;
END $$

DELIMITER ; 





/*DROP FUNCTION IF EXISTS normal_name;

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
RETURN (v);
SHOW WARNINGS;
END $$

DELIMITER ; */
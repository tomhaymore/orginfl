<?php

/**
 * Description of dbclass
 *
 * @author thaymore
 */
class database {

    function __construct($db = null)
    {
        // establish db connection
        $this->link = mysql_connect('localhost', 'root', 'pw');
        if($db != null) $db = mysql_select_db($db,$this->link);
        
    }

    public function select_db($db)
    {
        // select database
        $db = mysql_select_db('cdrg',$this->link);
    }

    public function where($params,$value = null,$op = null)
    {
        $query = "WHERE ";
        if($value == null) {
            if(is_array($params)) {
                $i =0;
                $count = count($params);
                foreach($params as $k=>$v) {
                    $query .= $k." = '".$v."'";
                    if($i < $count) {
                        $query .=', ';
                    }
                    $i++;
                }
                $this->where = $query;
            }
        } else {
            $op = ($op == null) ? '=' : $op;
            $query = sprintf("WHERE %s %s '%s'",mysql_real_escape_string($params),mysql_real_escape_string($op),mysql_real_escape_string($value));
            $this->where = $query;
        }
    }

    public function get($table,$params = null)
    {
        
        if($params == null) {
            if(!isset($this->where)) {
                $params = null;
            } else $params = $this->where;

        }

        $query = "SELECT * FROM ".$table.' '.$params;

        $result = mysql_query($query) or die(mysql_error());

        $this->clear();

        return $result;
    }

    public function insert($table,$options)
    {
        // if options is not an array, then return false
        if(!is_array($options)) return false;

        $query = sprintf("INSERT INTO %s(",mysql_real_escape_string($table));
        $values = "VALUES (";
        $count = count($options);
        $i = 1;
        foreach($options as $k=>$v) {
            $query .= mysql_real_escape_string($k);
            if(is_string($v)) {
                $values .= "'".mysql_real_escape_string($v)."'";
            } else {
                $values .= mysql_real_escape_string($v);
            }
            if($i < $count) {
                $query .= ',';
                $values .= ',';
            } else {
                $query .= ')';
                $values .= ')';
            }
            $i++;
        }
        $query = $query.' '.$values;
        $result = mysql_query($query) or die(mysql_error().$query);
        
        $this->insert_id = mysql_insert_id();
        return true;
        $this->clear();
    }

    public function update($table,$options)
    {
        // if options is not an array, then return false
        if(!is_array($options)) return false;
        if(!isset($this->where)) return false;

        $query = sprintf("UPDATE %s SET ",mysql_real_escape_string($table));
        $count = count($options);
        $i = 1;
        foreach($options as $k=>$v) {
            $query .= mysql_real_escape_string($k) . ' = ';
            if(is_string($v)) {
                $query .= "'".mysql_real_escape_string($v)."'";
            } else {
                // do I not need to escape this because it's an integer?
                $query .= $v;
            }
            if($i < $count) {
                $query .= ',';
            } /*else {
                $query .= ')';
                $values .= ')';
            }*/
            $i++;
        }
        $query = $query . $this->where;
        $result = mysql_query($query) or die(mysql_error().$query);

        $this->insert_id = mysql_insert_id();
        return true;
        $this->clear();
    }

    private function clear()
    {
        $this->where = null;
    }
    
}
?>

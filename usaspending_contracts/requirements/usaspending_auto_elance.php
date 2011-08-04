<?php

require_once('usaspending.php');
require_once('database.php');

function get_orgs_list()
{
    // retrieve orgs from db
    $result = mysql_query("SELECT org_id,org_name FROM orgs where org_status = 'active'");
    while($row = mysql_fetch_object($result)) {
        $orgs[]= array (
                'org_id' =>  $row->org_id,
                'org_name' => $row->org_name
        );
    }

    return $orgs;
}

function get_aliases_list()
{
    // initialize array for aliases
    $aliases = array();

    // retrieve aliases from dbd
    $result = mysql_query("SELECT org_id,org_aliases FROM orgs where org_status = 'active' AND org_aliases != NULL");
    while($row = mysql_fetch_object($result)) {
        $alias = unserialize($row->org_aliases);
        // if any of the aliases have an array, cycle through and put them in db
        if(is_array($alias)) {
            foreach($alias as $a) {
                $aliases[] = array(
                                'org_id' => $row->org_id,
                                'org_alias' => $a
                                );
            }
        }
    }

    return $aliases;
}

function check_process_status($f)
{
    $query = sprintf("SELECT * FROM files_processed WHERE file_name = '%s'",mysql_real_escape_string($f));
    $result = mysql_query($query) or die(mysql_error().$query);
    if(mysql_num_rows($result) == 1) {
        $row = mysql_fetch_row($result);
        return $row;
    } return null;

}

function update_file_status($file,$status,$line,$lines_processed,$lines_skipped)
{
    $query = sprintf("SELECT * from files_processed WHERE file_name = '%s'",mysql_real_escape_string($file));
    $result = mysql_query($query);
    if(mysql_num_rows($result) > 0) {
        $query = sprintf("UPDATE files_processed SET file_status = '%s',file_line = $line, file_lines_processed = $lines_processed, file_lines_skipped = $lines_skipped WHERE file_name = '%s'", mysql_real_escape_string($status),mysql_real_escape_string($file));
        $result = mysql_query($query) or die(mysql_error().$query);
    } else {
        $query = sprintf("INSERT INTO files_processed(file_status,file_name,file_line,file_lines_processed,file_lines_skipped) VALUES ('%s','%s',$line,$lines_processed,$lines_skipped)", mysql_real_escape_string($status), mysql_real_escape_string($file));
        $result = mysql_query($query) or die(mysql_error().$query);

    }
}

function process_file($file,$status,$orgs,$aliases)
{
    update_file_status($file,'in progress',$status[3],$status[4],$status[5]);
    // open file
    $f = fopen('/Users/thaymore/Documents/Research/CDRG/Data/USASpending/'.$file, 'r');
    // loop through file
    $i = 0;
    $lines_processed = $status[4];
    $lines_skipped = $status[5];
    while (($data = fgetcsv($f, 0, ',')) !== false) {
        if($i > $status[3] && $data[0] != 'unique_transaction_id') {
            // initialize USASpending library with data
            $usa = new USASpending($data);
            $usa->set_org_list($orgs);
            $usa->set_aliases_list($aliases);
            // check to see if Faca runs without a hitch or not
            if($usa->autoParse() == 'success') {
                // update new file line
                $lines_processed++;
                update_file_status($file,'in progress',$i,$lines_processed,$lines_skipped);
            } else {
                // update new file line
                $lines_skipped++;
                update_file_status($file,'in progress',$i,$lines_processed,$lines_skipped);
            }
        }
        $i++;
    }
    update_file_status($file,'completed',$i,$lines_processed,$lines_skipped);
}

// increase max memory
ini_set('memory_limit','512M');

// se the timezone
date_default_timezone_set('America/Los_Angeles');

// initialize db class
$db = new database('cdrg');

// select a db
$db->select_db('crdg');

// get list of matching elements

$orgs = get_orgs_list();

$aliases = get_aliases_list();

// set the working directory
$path = '/path/to/files';

// get directory handle
$dir = opendir($path);

// loop through directory
while($file = readdir($dir)) {
    // check to see if file is already processed
    if(!is_dir($file) && stristr($file,'.csv')) {
        echo $file;
        if(($status = check_process_status($file)) != null) {
            if($status[7] == 'in progress') {
                process_file($file,$status,$orgs,$aliases);
            }
        } else {
            process_file($file,array(0,0,0,0,0,0),$orgs,$aliases);
        }
    }

}




?>

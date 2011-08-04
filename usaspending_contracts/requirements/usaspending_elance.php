<?php

/**
 * USASpending
 *
 * USASpending information parser for PHP.
 *
 * @package		USASpending
 * @version		0.0.1
 */

 class USASpending {

 	function __construct($data)
 	{
            // initialize database class
            require_once('database.php');
            $this->db = new database('cdrg');
            $this->data = $data;
            $this->patterns = $this->set_patterns();
            $this->replacements = $this->set_replacements();
           
 	}

        private function set_patterns()
        {
            $patterns = array();
            if(($result = mysql_query("SELECT * FROM orgs_norm")) != false) {
                while($row = mysql_fetch_object($result)) {
                    $patterns = $row[1];
                }
            }
            return $patterns;
        }

        private function set_replacements()
        {
            $replacements = array();
            if(($result = mysql_query("SELECT * FROM orgs_norm")) != false) {
                while($row = mysql_fetch_object($result)) {
                    $replacements = $row[2];
                }
            }
            return $replacements;
        }

        public function set_org_list($orgs)
        {
            // initialize array for orgs
            $normalized_orgs = array();



            // cycle through orgs and normalize
            foreach($orgs as $o) {
                /*$name = trim(preg_replace($this->patterns,$this->replacements,$o['org_name']));
                $normalized_orgs[$o['org_id']] = preg_replace('/\s+/',' ',$name);*/
                $normalized_orgs[$o['org_id']] = $this->normalize($o['org_name']);

            }

            $this->orgs = $normalized_orgs;
            /*print_r($this->orgs);*/

        }

        private function normalize($name)
        {
            $name =  trim(preg_replace($this->patterns,$this->replacements,$name));
            return preg_replace('/\s+/',' ',$name);
        }

        public function set_aliases_list($aliases)
        {
            $this->aliases = $aliases;

        }

 	function autoParse($data = null)
 	{
            $data = (!$data) ? $this->data : $data;

            // check to make sure it's not the header row of data
            if($data[0] !== 'unique_transaction_id')
            {
                // check to see if it can find an organizational match
                if(($org_id = $this->_getOrg($data)) != null)
                {
                    // if it does, assign the rest of the data as well
                    $agency_id = $this->_getAgency($data);
                    $aff_id = $this->_addAff($org_id,$agency_id,$data);
                    return "success";
                } else {
                    // no vendor listed

                    return 'error';
                }
            }

 	}

 	
        private function _getAgency($a)
 	{
            if(($id = $this->check_agency(trim($a[5]))) != null)
            {
                return $id;
            } else {
                return $this->_addAgency($a);
            }
 	}

 	/**
 	 * check_agency
 	 *
 	 * checks to see if a particular agency has already been added to orgs table by comparing org abbreviations
 	 *
 	 * @param	str	$a
 	 * @return	int
 	*/

 	private function check_agency($a)
 	{
            $this->db->where('org_agency_code',$a);
            $result = $this->db->get('orgs_agencies');
            if(mysql_num_rows($result) == 1)
            {
                $row = mysql_fetch_object($result);
                return $row->org_agency_o_id;
            } 
            
            $db->where('org_name',$agency);
            $result = $db->get('orgs');
    
            if(mysql_num_rows($result) == 1) {
                $row = mysql_fetch_object($result);
                // insert translation

                $translation = array(
                                'org_agency_code'   => $data[5],
                                'org_agency_o_id'   => $row->org_id
                                );
                
                $this->db->insert('orgs_agencies',$translation);

                return $row->org_id;
            }


            return null;
 	}

 	

 	private function _addAgency($a)
 	{

            $names = explode(':',$a[5]);
            $name = 'U.S. '.trim($names[1]);

            $options = array('org_name' => $name,
                                'org_name_length'   => strlen($name),
                                'org_type'          => 'org',
                                'org_sub_types'     => 'Org, GovernmentEntity,Federal,Agency'
                                );

            if($this->db->insert('orgs',$options)) {

                $org_id = $this->db->insert_id;

                // insert translation here

                $translation = array(
                                'org_agency_code'   => $a[5],
                                'org_agency_o_id'   => $org_id
                                );

                $this->db->insert('orgs_agencies',$translation);

                // insert meta info here

                $meta = array(
                                'org_meta_org_id'   => $org_id,
                                'org_meta_is_govt'  => 1,
                                'org_meta_is_fed'   => 1
                                );

                $this->db->insert('orgs_meta',$meta);

                $ext = array(
                            'org_ext_local_type'    => 'org',
                            'org_ext_local_id'      => $org_id,
                            'org_ext_remote_src'    => 'usaspending'
                            );

                $this->db->insert('orgs_ext',$ext);

                return true;

            } else return false;
 	}

 	private function _addAff($org_id,$agency_id,$data)
 	{
            // add new affiliation between indiv and comm
            $aff = array(
                        'aff_subtype' => 'contract',
                        'aff_e1_id' => $agency_id,
                        'aff_e1_type' => 'org',
                        'aff_e2_id' => $org_id,
                        'aff_e2_type' => 'org',
                        'aff_start' => date('Y-m-d',strtotime($data[14])),
                        'aff_end' => date('Y-m-d',strtotime($data[16])),
                        'aff_created' => date('Y-m-d H:i:s')
                        );

            if($this->db->insert('affs',$aff)) {
                $aff_id = $this->db->insert_id;
                $aff_meta = array(
                                'aff_meta_aff_id'   => $aff_id,
                                'aff_meta_subtype' => 'transaction,governmentContract',
                                'aff_meta_descr1' => $data[0],
                                'aff_meta_descr2' => $data[32].'; '.$data[39],
                                'aff_meta_amount'   => $data[2],
                                'aff_meta_trans_descr1' => $data[79],
                                'aff_meta_trans_descr2' => $data[80],

                                
                                );

                $this->db->insert('affs_meta',$aff_meta);
                return true;
            } else return null;
 	}

        private function _getOrg($data)
        {
            // if name of organization is null, skip it
            if($data[44] == '') return null;

            // use each of the possible names to check if organization exists
            $names = array($data[44],$data[45],$data[46],$data[47]);

            // cycle through the names
            foreach($names as $name) {
                // check to see if there is actually an entrance here
                if($name != '') {
                    if(($org_id = $this->_parseOrg($name)) != null) {
                        $this->update_org_meta($org_id,$data);
                        return $org_id;
                    }
                }
            }

            return $this->_addOrg($data);
        }

        private function update_org_meta($org_id,$data)
        {
            $meta = array(
                   'org_meta_org_id'    => $org_id,
                   'org_meta_employees' => $data[119],
                   'org_meta_employees_year' => $data[98],
                   'org_meta_revenue'   => $data[120],
                   'org_meta_revenue_year'  => $data[98]
                );

            $this->db->where('org_meta_org_id',$org_id);

            $result = $this->db->get('orgs_meta');
            if(mysql_num_rows($result) == 1) {
                $this->db->where('org_meta_org_id',$org_id);
                $this->db->update('orgs_meta',$meta);
            } else {
                $this->db->insert('orgs_meta',$meta);
            }

            $contact = array(
                        'org_contact_org_id'  => $org_id,
                        'org_contact_address1' => $data[53],
                        'org_contact_address2'  => $data[54],
                        'org_contact_address3'  => $data[55],
                        'org_contact_city'      => $data[56],
                        'org_contact_state'     => $data[57],
                        'org_contact_zip'       => $data[58],
                        'org_contact_country'   => $data[59],
                        'org_contact_cd'        => $data[61],
                        'org_contact_phone'     => $data[67],
                        'org_contact_fax'       => $data[68]
            );

            $this->db->insert('orgs_contact',$contact);

            $this->db->where('org_ref_org_id',$org_id);

            $result = $this->db->get('orgs_ref');

            $ref = array();
            if($data[65] != '' || $data[66] != '') {
                if(mysql_num_rows($result) == 1) {
                    $row = mysql_fetch_assoc($result);
                    if($row['org_ref_duns'] != '') {
                        if($duns = unserialize($row['org_ref_duns'])) {
                            if(!in_array($data[65],$duns)) {
                                $duns[] = $data[65];
                            }
                            if(!in_array($data[66],$duns)) {
                                $duns[] = $data[66];
                            }
                            $ref['org_ref_duns'] = serialize($duns);
                        }
                    }
                    if(!empty($ref)) {
                        $this->db->where('org_ref_org_id',$org_id);

                        $this->db->update('orgs_ref',$ref);
                    }
                } else {
                    $duns = array($data[65],$data[66]);
                    $ref['org_ref_duns'] = serialize($duns);
                    $ref['org_ref_org_id'] = $org_id;
                    $this->db->insert('orgs_ref',$ref);
                }
            }


        }

        private function _addOrg($data)
        {
            // need to check parent?
            $names = array($data[45],$data[46],$data[47]);

            $aliases = array();

            foreach($names as $n) {
                if($n != '') {
                    $aliases[] = $n;
                }
            }

            $org = array(
                        'org_name'          => ucwords(strtolower($data[44])),
                        'org_name_length'   => strlen($data[44]),
                        'org_type'          => 'Org',
                        'org_sub_types'     => 'Org',
                        'org_aliases'       => serialize($aliases),
                        'org_created'       => date('Y-m-d H:i:s')
            );

            $this->db->insert('orgs',$org);

            $org_id = $this->db->insert_id;

            if($org_id != null) {

                $meta = array(
                   'org_meta_org_id'    => $org_id,
                   'org_meta_employees' => $data[119],
                   'org_meta_employees_year' => $data[98],
                   'org_meta_revenue'   => $data[120],
                   'org_meta_revenue_year'  => $data[98]
                );

                $this->db->insert('orgs_meta',$meta);

                $contact = array(
                        'org_contact_org_id'  => $org_id,
                        'org_contact_address1' => $data[53],
                        'org_contact_address2'  => $data[54],
                        'org_contact_address3'  => $data[55],
                        'org_contact_city'      => $data[56],
                        'org_contact_state'     => $data[57],
                        'org_contact_zip'       => $data[58],
                        'org_contact_country'   => $data[59],
                        'org_contact_cd'        => $data[61],
                        'org_contact_phone'     => $data[67],
                        'org_contact_fax'       => $data[68]
                );

                $this->db->insert('orgs_contact',$contact);

                $ext = array(
                            'org_ext_local_type'    => 'org',
                            'org_ext_local_id'      => $org_id,
                            'org_ext_remote_src'    => 'usaspending'
                            );
                
                $this->db->insert('orgs_ext',$ext);

                return $org_id;
            }

            
        }

 	private function _parseOrg($name)
 	{
            $this->db->where('org_name',$name,'like');

            $result = $this->db->get('orgs');

            if(mysql_num_rows($result) == 1) {
                $row = mysql_fetch_object($result);
                return $row->org_id;
            }

            foreach($this->orgs as $k=>$v) {
                
                if(stristr($this->normalize($name),$v)) return $k;
            }

            foreach($this->aliases as $k=>$v) {
                
                if(stristr($name,$v)) return $k;
            }

            // need to remove occupations from name string
            $start = substr($name,0,1);
            $name = $this->strip_org_name($name);
            $query = "SELECT org_id,org_name FROM orgs WHERE org_name like '$start%' and length(org_name) > 5 ORDER BY org_name_length 'desc'";;

            if(($result = mysql_query($query)) != false) {
                while($row = mysql_fetch_object($result)) {
                    $org_name = $this->normalize($row->org_name);
                    similar_text($name, $org_name,$score);
                    if($score >= 95) {
                        return $row->org_id;
                    }
                }
            }
            return null;
 	}

 	private function strip_org_name($name)
 	{
            $result = $this->db->get('subs_occ');
            if(mysql_num_rows($result) > 0) {
                $patterns = array();
                $replacement = array();
                while($row = mysql_fetch_object($result)) {
                        $patterns[] = $row->sub_occ_reg;
                        $replacement[] = '';
                }
                $name = preg_replace($patterns,$replacement,$name);
                return $name;
            }
            return $name;
 	}


 }
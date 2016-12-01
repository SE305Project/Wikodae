<?php
function connect_db($server_name = "127.0.0.1", $username = "root", $password = "", $db_name = "wikidata"){
	$con = mysql_connect("127.0.0.1",$username,$password);
	mysql_query("SET NAMES 'UTF8'");
	if (!$con){
		die('Could not connect: ' . mysql_error());
	}
	mysql_select_db($db_name, $con);
	return $con;
}

function query1($input, $lan){
	$con = connect_db();
	$query = "select entity.entity_id, entity.entity_text, description.desc_text 
			from entity, description 
			where entity_text='".$input."' and entity_language='".$lan."' 
			and description.entity_id=entity.entity_id and description.desc_language=entity_language";
	$result = mysql_query($query);
	mysql_close($con);
	return $result;
}

function query2($input, $lan){
	$con = connect_db();
	$query = "select entity.entity_text, entity.entity_id, mainsnak.property_id, entity_language
			from entity, mainsnak
			where (mainsnak.property_id='P31' or mainsnak.property_id='P279')
			and mainsnak.entity_id in (
				select ent.entity_id 
			    from entity as ent 
			    where ent.entity_text='".$input."')
			and entity.entity_id in (
				select wkb.id 
			    from datavalue_wikibase as wkb 
			    where wkb.snak_id=mainsnak.snak_id) and entity_language='".$lan."'
			order by entity.entity_id";
	$result = mysql_query($query);
	mysql_close($con);
	return $result;
}

function query3($input){
	$con = connect_db();
	$query = "select wkb1.id as result_id, wkb2.id as query_id 
			from (select snak_id, entity_id, property_id, datatype from mainsnak 
				where datatype='wikibase-item') as snak1, 
			datavalue_wikibase as wkb1,   
			(select snak_id, entity_id, property_id, datatype from mainsnak 
				where datatype='wikibase-item') as snak2, 
				datavalue_wikibase as wkb2  
				where wkb2.id in (   
					select distinct ent2.entity_id from entity as ent2   
				    where ent2.entity_text='".$input."')
				and snak1.snak_id=wkb1.snak_id  
				and snak2.snak_id=wkb2.snak_id  
				and snak2.datatype='wikibase-item'   
				and wkb1.id<>wkb2.id   
				and snak1.property_id=snak2.property_id  
				and snak1.entity_id=snak2.entity_id
				order by wkb2.id";
	$result = mysql_query($query);
	mysql_close($con);
	return $result;
}

function query4_properties($input, $lan){
	$con = connect_db();
	$query = "select e1.entity_text as property_text, e1.entity_id as property_id, snak.entity_id, des1.desc_text as property_desc_text, des2.desc_text as desc_text, e2.entity_text
			from entity as e1, mainsnak as snak, description as des1, description as des2, entity as e2
			where e1.entity_id=snak.property_id
			and e1.entity_language='".$lan."'
			and e2.entity_text='".$input."' and e2.entity_language=e1.entity_language
			and des2.entity_id=e2.entity_id and des2.desc_language=e1.entity_language
			and snak.entity_id=e2.entity_id
			and des1.entity_id=e1.entity_id and des1.desc_language=e1.entity_language";
	$result = mysql_query($query);
	mysql_close($con);
	return $result;
}

function query4_statements($input, $lan){
	$con = connect_db();
	$query = "select snak.snak_id, snak.entity_id, des.desc_text, ent.entity_text
			from mainsnak as snak, entity as ent, description as des
			where snak.entity_id=ent.entity_id
			and ent.entity_text='".$input."' and ent.entity_language='".$lan."'
			and des.entity_id=ent.entity_id and des.desc_language=ent.entity_language
			order by entity_id";
	$result = mysql_query($query);
	mysql_close($con);
	return $result;
}

function entity_text_by_id($id, $lan){
	$con = connect_db();
	$query = "select entity_text from entity
			where entity_id='".$id."'
				and entity_language='".$lan."'";
	$result = mysql_query($query);
	mysql_close($con);
	return $result;
}

function all_language(){
	$con = connect_db();
	$query = "select distinct entity_language from entity
			where not entity_language='en'";
	$result = mysql_query($query);
	mysql_close($con);
	return $result;
}

function all_property(){
	$con = connect_db();
	$query = "select entity_id, entity_text from entity
			where entity_type='property' and entity_language='en'";
	$result = mysql_query($query);
	mysql_close($con);
	return $result;
}

function qa_base($entity_name, $property_name){
	$con = connect_db();
	$query = "select snak_id, entity_id, property_id, datatype from mainsnak as snak
			where entity_id in (
				select ent1.entity_id from entity as ent1 
			    where entity_language='en' and entity_text='".$property_name."')and property_id in (
			select ent2.entity_id from entity as ent2
		    where entity_language='en' and entity_text='".$entity_name."')";
	$result = mysql_query($query);
	mysql_close($con);
	return $result;
}

function qa_value($snak_id, $datatype){
	$con = connect_db();
	switch ($datatype) {
		case 'globe-coordinate':
			$table='datavalue_globecoordinate';
			break;
		case 'quantity':
			$table='datavalue_quantity';
			break;
		case 'string':
			$table='datavalue_string';
			break;
		case 'time':
			$table='datavalue_time';
			break;
		case 'wikibase-item':
			$table='datavalue_wikibase';
			break;
		default:
			$table='datavalue_wikibase';
			break;
	}
	$query = "select * from ".$table."
			where snak_id='".$snak_id."'";
	$result = mysql_query($query);
	mysql_close($con);
	return $result;
}

?>
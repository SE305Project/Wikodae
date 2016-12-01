select snak_id, entity_id, property_id, datatype from mainsnak as snak
where entity_id in (
	select ent1.entity_id from entity as ent1 
    where entity_language='en' and entity_text='earth')
and property_id in (
	select ent2.entity_id from entity as ent2
    where entity_language='en' and entity_text='population')
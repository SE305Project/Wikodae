select entity.entity_text, entity.entity_id, mainsnak.property_id, entity_language
from entity, mainsnak
where (mainsnak.property_id="P31" or mainsnak.property_id="P279")
and mainsnak.entity_id in (
	select ent.entity_id 
    from entity as ent 
    where ent.entity_text="gas")
and entity.entity_id in (
	select wkb.id 
    from datavalue_wikibase as wkb 
    where wkb.snak_id=mainsnak.snak_id) and entity.entity_language='en'
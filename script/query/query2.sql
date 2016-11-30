select * from entity
where entity_id in (select wkb.id from datavalue_wikibase as wkb
where wkb.snak_id in (select snak.snak_id from mainsnak as snak
where (snak.property_id="P31" or snak.property_id="P279") and snak.entity_id=(
select distinct e.entity_id from entity as e 
where e.entity_text='universe'))) and entity_language="en"
select wkb1.id as entity_id, wkb2.id as query_id
from (select snak_id, entity_id, property_id, datatype from mainsnak where datatype="wikibase-item") as snak1, 
datavalue_wikibase as wkb1,   
(select snak_id, entity_id, property_id, datatype from mainsnak where datatype="wikibase-item") as snak2, 
datavalue_wikibase as wkb2
where wkb2.id in (   
	select distinct ent2.entity_id from entity as ent2   
    where ent2.entity_text="gas")   
and snak1.snak_id=wkb1.snak_id  
and snak2.snak_id=wkb2.snak_id  
and snak2.datatype="wikibase-item"   
and wkb1.id<>wkb2.id   
and snak1.property_id=snak2.property_id  
and snak1.entity_id=snak2.entity_id
order by wkb2.id

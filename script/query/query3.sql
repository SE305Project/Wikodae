select * from entity as ent
where ent.entity_id in (
	select wkb1.id 
    from (select * from mainsnak where datatype="wikibase-item") as snak1 
    natural join datavalue_wikibase as wkb1
	where exists(
		select wkb2.id 
        from (select * from mainsnak where datatype="wikibase-item") as snak2
        natural join datavalue_wikibase as wkb2
		where snak2.datatype="wikibase-item" 
		and wkb1.id<>wkb2.id 
		and snak1.property_id=snak2.property_id
        and snak1.entity_id=snak2.entity_id
		and wkb2.id in (
			select ent2.entity_id from entity as ent2
			where ent2.entity_text="universe")))
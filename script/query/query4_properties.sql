-- properties
select e1.entity_text, e1.entity_id from entity as e1
where e1.entity_id in (
	select mainsnak.property_id from mainsnak
    where mainsnak.entity_id in (
		select e2.entity_id from entity as e2
		where e2.entity_text="universe")) and e1.entity_language='en'
        
-- statements

-- statements
select snak.snak_id, snak.entity_id from mainsnak as snak
where snak.entity_id in (
	select ent.entity_id from entity as ent
    where ent.entity_text='gas'
    and ent.entity_language='en')
order by entity_id
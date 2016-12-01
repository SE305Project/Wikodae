-- statements
select snak.snak_id, snak.entity_id, des.desc_text, ent.entity_text
from mainsnak as snak, entity as ent, description as des
where snak.entity_id=ent.entity_id
and ent.entity_text='gas' and ent.entity_language='en'
and des.entity_id=ent.entity_id and des.desc_language=ent.entity_language
order by entity_id
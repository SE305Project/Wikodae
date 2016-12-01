-- properties
select e1.entity_text as property_text, e1.entity_id as property_id, snak.entity_id, des1.desc_text as property_desc_text, des2.desc_text as desc_text, e2.entity_text
from entity as e1, mainsnak as snak, description as des1, description as des2, entity as e2
where e1.entity_id=snak.property_id
and e1.entity_language='en'
and e2.entity_text="universe" and e2.entity_language=e1.entity_language
and des2.entity_id=e2.entity_id and des2.desc_language=e1.entity_language
and snak.entity_id=e2.entity_id
and des1.entity_id=e1.entity_id and des1.desc_language=e1.entity_language

-- statements

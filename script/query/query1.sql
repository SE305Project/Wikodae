SELECT entity.entity_id, entity.entity_text, description.desc_text FROM entity, description 
where entity_text='universe' and entity_language='en' and description.desc_language='en'
and description.entity_id=entity.entity_id
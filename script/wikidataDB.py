import json
import pymysql
import time

def insert():

    testFile = open("smallwikidata-latest-all3.json")

    data = json.load(testFile)[0]

    print(type(data))

    entity_id = data["id"]
    entity_type = data["type"]
    entity_desc = data["descriptions"]["en"]["value"]
    claims = data["claims"]

    print ("entity_id: " + entity_id)
    print ("entity_type: " + entity_type)
    print ("descriptions: " + str(entity_desc))
    print ("\n")

    # if entity_type=="item":
        # cursor.execute("INSERT INTO items VALUES (%s, %s)", (entity_id, entity_desc))  
    # elif entity_type=="property":
        # cursor.execute("INSERT INTO properties VALUES (%s, %s)", (entity_id, entity_desc))

    for key in claims.keys():
        property_id = key
        property = claims[key]
        property_type = property[0]["type"]
        mainsnak = property[0]["mainsnak"]
        datavalue = mainsnak["datavalue"]
        datavalue_type = datavalue["type"]
        datavalue_value = datavalue["value"]
        snak_id = property[0]["id"]
        snak_type = mainsnak["snaktype"]
        wikibase_entityid = ""

        if datavalue_type=="wikibase-entityid":
            wikibase_entityid = datavalue_value["id"]
            datavalue_value = "" #temp fix

        print ("property_id: " + property_id)
        print ("property_type: " + property_type)
        print ("snak_type: " + snak_type)
        print ("snak_id: " + snak_id)
        print ("datavalue_type: " + datavalue_type)
        print ("datavalue_value: " + str(datavalue_value))
        print ("\n")

        # TODO: fix inserting datavalue_value for wikibase_entity, coordinates, time, etc
        # cursor.execute("INSERT INTO snak VALUES (%s, %s, %s, %s, %s, %s, %s)", (snak_id, entity_id, property_id, snak_type, datavalue_type, datavalue_value, wikibase_entityid))



if __name__ == '__main__':
    print('start')
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='',
                                 db='wikidata_1',
                                 charset='utf8mb4',
                                 port=3306,
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    print('connected')
    insert()
    # connection.commit()

    cursor.close()
    connection.close()
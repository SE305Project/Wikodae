import json
import pymysql
import time

def insert():

    testFile = open("smallwikidata-latest-all3.json")

    for data in json.load(testFile):

        # print(type(data))

        entity_id = data["id"]
        entity_lang = "en"
        entity_type = data["type"]
        entity_desc = data["descriptions"]["en"]["value"]
        desc_lang = data["descriptions"]["en"]["language"]
        entity_text = data["labels"]["en"]["value"]
        claims = data["claims"]

        # print("entity_id: " + entity_id)
        # print("entity_type: " + entity_type)
        # print("descriptions: " + str(entity_desc))
        # print("\n")

        cursor.execute("INSERT INTO entity(entity_id, entity_language, entity_type, entity_text) VALUES (%s, %s, %s, %s)", (entity_id, entity_lang, entity_type, entity_text))
        cursor.execute("INSERT INTO description(entity_id, desc_language, desc_text) VALUES (%s, %s, %s)", (entity_id, desc_lang, entity_desc))

        for key in claims.keys():
            property_id = key
            property = claims[key]
            for serial in range(0,len(property)):  
                claim_type = property[serial]["type"]
                rank = property[serial]["rank"]
                mainsnak = property[serial]["mainsnak"]
                datavalue = mainsnak["datavalue"]
                datavalue_type = datavalue["type"]
                datavalue_value = datavalue["value"]
                snak_id = property[serial]["id"]
                snak_type = mainsnak["snaktype"]

                if "qualifiers" in property[serial]:
                    qualifiers = property[serial]["qualifiers"]
                    for pid in qualifiers.keys():
                        for i in range(0,len(qualifiers[pid])):
                            q_hash = qualifiers[pid][i]["hash"]
                            print(q_hash)
                            q_snak_type = qualifiers[pid][i]["snaktype"]
                            q_property_id = pid
                            q_data_type = qualifiers[pid][i]["datatype"]
                            cursor.execute("INSERT INTO qualifier(hash, snaktype, property_id, datatype) VALUES (%s, %s, %s, %s)", (q_hash, q_snak_type, q_property_id, q_data_type))

                cursor.execute("INSERT INTO mainsnak VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (snak_id, entity_id, property_id, serial, claim_type, snak_type, datavalue_type, rank))

                if datavalue_type == "string":
                    value = datavalue_value
                    cursor.execute("INSERT INTO datavalue_string VALUES (%s, %s)", (snak_id, value))
                elif datavalue_type == "wikibase-entityid":
                    wikibase_entityid = datavalue_value["id"]
                    cursor.execute("INSERT INTO datavalue_wikibase VALUES (%s, %s)", (snak_id, wikibase_entityid))
                elif datavalue_type == "time":
                    time = datavalue_value["time"]
                    timezone = datavalue_value["timezone"]
                    before = datavalue_value["before"]
                    after = datavalue_value["after"]
                    precision = datavalue_value["precision"]
                    calendarmodel = datavalue_value["calendarmodel"]
                    cursor.execute("INSERT INTO datavalue_time VALUES (%s, %s, %s, %s, %s, %s, %s)", (snak_id, time, timezone, before, after, precision, calendarmodel))
                elif datavalue_type == "globecoordinate":
                    latitude = datavalue_value["latitude"]
                    longitude = datavalue_value["longitude"]
                    altitude = datavalue_value["altitude"]
                    precision = datavalue_value["precision"]
                    globe = datavalue_value["globe"]
                    cursor.execute("INSERT INTO datavalue_globecoordinate VALUES (%s, %s, %s, %s, %s, %s)", (snak_id, latitude, longitude, altitude, precision, globe))
                elif datavalue_type == "quantity":
                    amount = datavalue_value["amount"]
                    upperBound = datavalue_value["upperBound"]
                    lowerBound = datavalue_value["lowerBound"]
                    #unit = datavalue_value["unit"]
                    cursor.execute("INSERT INTO datavalue_quantity VALUES (%s, %s, %s, %s, 'default')", (snak_id, amount, upperBound, lowerBound))


                # print("property_id: " + property_id)
                # print("claim_type: " + claim_type)
                # print("snak_type: " + snak_type)
                # print("snak_id: " + snak_id)
                # print("datavalue_type: " + datavalue_type)
                # print("datavalue_value: " + str(datavalue_value))
                # print("\n")    

if __name__ == '__main__':
    # print('start')
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='',
                                 db='wikidata',
                                 charset='utf8mb4',
                                 port=3306,
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    # print('connected')
    insert()
    connection.commit()

    cursor.close()
    connection.close()
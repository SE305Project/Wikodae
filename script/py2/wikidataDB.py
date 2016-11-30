import json
import pymysql
import time
import sys

def truncateall():
    cursor.execute("TRUNCATE TABLE datavalue_globecoordinate")
    cursor.execute("TRUNCATE TABLE datavalue_quantity")
    cursor.execute("TRUNCATE TABLE datavalue_string")
    cursor.execute("TRUNCATE TABLE datavalue_time")
    cursor.execute("TRUNCATE TABLE datavalue_wikibase")
    cursor.execute("TRUNCATE TABLE description")
    cursor.execute("TRUNCATE TABLE entity")
    cursor.execute("TRUNCATE TABLE mainsnak")
    cursor.execute("TRUNCATE TABLE qualifier")

def truncate_str(s, length, encoding='utf-8'):
    encoded = s.encode(encoding)[:length]
    return encoded.decode(encoding, 'ignore')

def insert(line):
    if len(line)>2 and line[-2]==",":
        line = line[:-2]
    if len(line)<=2 or line == "[\n" or line == "]\n":
        return
    data = json.loads(line)

    entity_id = data["id"]
    entity_type = data["type"]
    if not data["descriptions"]: #data.descriptions is empty
        cursor.execute("LOCK TABLES description WRITE")
        cursor.execute("INSERT INTO description(entity_id, desc_language, desc_text) VALUES (%s, 'N/A', 'N/A')", (entity_id))
        cursor.execute("UNLOCK TABLES")
    else:
        for desc_lang in data["descriptions"].keys():
            entity_desc = data["descriptions"][desc_lang]["value"]

            # bytes = str.encode(entity_desc)
            # if sys.getsizeof(bytes) > 255:
            #     truncated = truncate_str(entity_desc, 220)
            #     entity_desc = truncated
            #     print(sys.getsizeof(bytes))
            #     print(sys.getsizeof(str.encode(truncated)))
            #     print("\n")

            cursor.execute("LOCK TABLES description WRITE")
            cursor.execute("INSERT INTO description(entity_id, desc_language, desc_text) VALUES (%s, %s, %s)", (entity_id, desc_lang, entity_desc))
            cursor.execute("UNLOCK TABLES")
    if not data["labels"]:
        cursor.execute("INSERT INTO entity(entity_id, entity_language, entity_type, entity_text) VALUES (%s, 'N/A', %s, 'N/A')", (entity_id, entity_type))
    else:
        for entity_lang in data["labels"].keys():
            print(entity_lang)
            entity_text = data["labels"][entity_lang]["value"]
            cursor.execute("LOCK TABLES entity WRITE")
            cursor.execute("INSERT INTO entity(entity_id, entity_language, entity_type, entity_text) VALUES (%s, %s, %s, %s)", (entity_id, entity_lang, entity_type, entity_text))
            cursor.execute("UNLOCK TABLES")
    # print("entity_id: " + entity_id)
    # print("entity_type: " + entity_type)
    # print("descriptions: " + str(entity_desc))
    # print("\n")

    claims = data["claims"]
    for key in claims.keys():
        property_id = key
        property = claims[key]
        for serial in range(len(property)):  
            claim_type = property[serial]["type"]
            rank = property[serial]["rank"]
            mainsnak = property[serial]["mainsnak"]
            snak_id = property[serial]["id"]
            snak_type = mainsnak["snaktype"]
            data_type = mainsnak["datatype"]

            cursor.execute("LOCK TABLES mainsnak WRITE")
            cursor.execute("INSERT INTO mainsnak VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (snak_id, entity_id, property_id, serial, claim_type, snak_type, data_type, rank))
            cursor.execute("UNLOCK TABLES")

            if "qualifiers" in property[serial]:
                qualifiers = property[serial]["qualifiers"]
                for pid in qualifiers.keys():
                    for i in range(0,len(qualifiers[pid])):
                        q_hash = qualifiers[pid][i]["hash"]
                        q_snak_type = qualifiers[pid][i]["snaktype"]
                        q_property_id = pid
                        q_data_type = qualifiers[pid][i]["datatype"]
                        q_datavalue = qualifiers[pid][i]["datavalue"]["value"]
                        insert_datavalue(q_data_type, q_datavalue, snak_id+pid)
                        cursor.execute("LOCK TABLES qualifier WRITE")
                        cursor.execute("INSERT INTO qualifier(hash, snaktype, property_id, datatype) VALUES (%s, %s, %s, %s)", (q_hash, q_snak_type, q_property_id, q_data_type))
                        cursor.execute("UNLOCK TABLES")

            if "datavalue" in mainsnak:
                datavalue = mainsnak["datavalue"]
                datavalue_type = datavalue["type"]
                datavalue_value = datavalue["value"]
                insert_datavalue(datavalue_type, datavalue_value, snak_id)


def insert_datavalue(datavalue_type, datavalue_value, snak_id):
    if datavalue_type == "string":
        cursor.execute("LOCK TABLES datavalue_string WRITE")
        cursor.execute("INSERT INTO datavalue_string VALUES (%s, %s)", (snak_id, datavalue_value))
        cursor.execute("UNLOCK TABLES")
    elif datavalue_type == "wikibase-entityid":
        wikibase_entityid = datavalue_value["id"]
        cursor.execute("LOCK TABLES datavalue_wikibase WRITE")
        cursor.execute("INSERT INTO datavalue_wikibase VALUES (%s, %s)", (snak_id, wikibase_entityid))
        cursor.execute("UNLOCK TABLES")
    elif datavalue_type == "time":
        time = datavalue_value["time"]
        timezone = datavalue_value["timezone"]
        before = datavalue_value["before"]
        after = datavalue_value["after"]
        precision = datavalue_value["precision"]
        calendarmodel = datavalue_value["calendarmodel"]
        cursor.execute("LOCK TABLES datavalue_time WRITE")
        cursor.execute("INSERT INTO datavalue_time VALUES (%s, %s, %s, %s, %s, %s, %s)", (snak_id, time, timezone, before, after, precision, calendarmodel))
        cursor.execute("UNLOCK TABLES")
    elif datavalue_type == "globecoordinate":
        latitude = datavalue_value["latitude"]
        longitude = datavalue_value["longitude"]
        altitude = datavalue_value["altitude"]
        precision = datavalue_value["precision"]
        globe = datavalue_value["globe"]
        cursor.execute("LOCK TABLES datavalue_globecoordinate WRITE")
        cursor.execute("INSERT INTO datavalue_globecoordinate VALUES (%s, %s, %s, %s, %s, %s)", (snak_id, latitude, longitude, altitude, precision, globe))
        cursor.execute("UNLOCK TABLES")
    elif datavalue_type == "quantity":
        amount = datavalue_value["amount"]
        upperBound = datavalue_value["upperBound"]
        lowerBound = datavalue_value["lowerBound"]
        unit = datavalue_value["unit"]
        cursor.execute("LOCK TABLES datavalue_quantity WRITE")
        cursor.execute("INSERT INTO datavalue_quantity VALUES (%s, %s, %s, %s, %s)", (snak_id, amount, upperBound, lowerBound, unit))
        cursor.execute("UNLOCK TABLES")

            # print("property_id: " + property_id)
            # print("claim_type: " + claim_type)
            # print("snak_type: " + snak_type)
            # print("snak_id: " + snak_id)
            # print("datavalue_type: " + datavalue_type)
            # print("datavalue_value: " + str(datavalue_value))
            # print("\n")    

if __name__ == '__main__':
    print("start")
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='',
                                 db='wikidata',
                                 charset='utf8mb4',
                                 port=3306,
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    print("connected")
    clear = True
    if clear:
        truncateall()
    print("start insert")
    begin = 1
    end = 2 #end is not included
    f = open("smallwikidata-latest-all3.json","r")
    for i in range(begin):
        f.readline()
    for i in range(begin,end):
        print(i)
        line = f.readline()
        insert(line)
    connection.commit()
    f.close()
    cursor.close()
    connection.close()
#
#   DoCompose.py
#
#   David Janes
#   IOTDB
#   2015-03-07
#
#   Take all the files in "src/" and
#   compose the JSON-LD files.
#
#   See README.md for more details
#

import sys
import os
import json
import re

SRC_FOLDER = "src/"
DST_FOLDER = "var/"
TOP_NAMES = [
    "iot",
    "iot-purpose",
    "iot-facet",
    "iot-unit",
]

SCHEMA_NAMES = [ 
    "name", 
    "description", 
    "url", 
    "image", 
    "sameAs", 
]

NUMERIC_NAMES = [
    "iot:minimum",
    "iot:maximum",
]

def cook_type(type_name):
    if re.match("^[A-Z]", type_name):
        return "iot:" + type_name
    elif type_name == "id":
        return "@id"
    elif type_name == "class":
        return "rdfs:Class"
    else:
        return "xs:" + type_name

def file_loader(fin):
    d = {}
    for line in fin:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        parts = line.split(' ', 1)
        if len(parts) != 2:
            continue

        tag, value = parts
        tag = tag.strip()
        value = value.strip()

        if tag.find(':') == -1:
            ## http://schema.org/Thing
            if tag in SCHEMA_NAMES:
                tag = "schema:" + tag
            else:
                tag = "iot:" + tag

        if tag in NUMERIC_NAMES:
            if value.find('.') == -1:
                value = int(value)
            else:
                value = float(value)

        d.setdefault(tag, []).append(value)

    for key, value in list(d.items()):
        if len(value) == 1:
            d[key] = value[0]

    return d

def top_loader(top_name):
    ds = []
    top_folder = os.path.join(SRC_FOLDER, top_name)

    for type_name in os.listdir(top_folder):
        if type_name.startswith("."):
            continue

        type_folder = os.path.join(top_folder, type_name)

        type_type = cook_type(type_name)

        for file_name in os.listdir(type_folder):
            if file_name.startswith("."):
                continue

            file_path = os.path.join(type_folder, file_name)
            filed = file_loader(open(file_path))
            filed["@type"] = type_type
            filed["@id"] = "https://iotdb.org/pub/%s#%s" % ( top_name, file_name )

            if top_name in [ "iot" ]:
                filed.setdefault("schema:name", file_name)
            else:
                filed.setdefault("schema:name", re.sub("^.*[.]", "", file_name))

            if type_type == "rdfs:Class":
                filed["rdfs:isDefinedBy"] = 'iot:' + file_name

            ds.append(filed)

    return ds

try:
    os.makedirs(DST_FOLDER)
except:
    pass

d_types = set()
for top_name in TOP_NAMES:
    contextd = {
        "schema": "https://schema.org/",
        "iot": "https://iotdb.org/pub/iot#",
        "iot-unit": "https://iotdb.org/pub/iot-unit#",
        "iot-purpose": "https://iotdb.org/pub/iot-purpose#",
        "iot-facet": "https://iotdb.org/pub/iot-facet#",
        "rdf" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs" : "http://www.w3.org/2000/01/rdf-schema#",
        "xs": "http://www.w3.org/2001/XMLSchema/#",
    }
    ds = top_loader(top_name)
    jsonld = {
        "@id": "https://iotdb.org/pub/%s" % top_name,
        "@context": contextd,
        "iot:item" : ds
    }

    ## identify types
    for d in ds:
        if d["@type"] != "@id":
            continue

        d_id = d["@id"]
        d_id = re.sub("^.*/", "", d_id)
        d_id = re.sub("#", ":", d_id)
        d_types.add(d_id)

    ## add to context (this makes NS URL values expand in JSON-LD)
    for d_type in d_types:
        d_url = "https://iotdb.org/pub/%s" % re.sub(":", "#", d_type)
        d_key = re.sub("^.*:", "", d_type)
        contextd[d_key] = {
            "@type": "@id",
            "@id": d_url,
        }
    """
    for d in ds:
        for key in d.iterkeys():
            if key not in d_types:
                continue

            contextd[key] = {
                "@type": "@id"
            }
    """


    top_dst = os.path.join(DST_FOLDER, "%s.jsonld" % top_name)
    with open(top_dst, 'w') as tout:
        print >> sys.stderr, "wrote: %s.jsonld" % top_name
        print >> tout, json.dumps(jsonld, sort_keys=True, indent=2)

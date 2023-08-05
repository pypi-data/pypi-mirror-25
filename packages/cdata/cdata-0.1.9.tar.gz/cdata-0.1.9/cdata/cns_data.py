#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Li Ding


import os
import sys
import json
import logging
import codecs
import hashlib
import datetime
import logging
import time
import re
import collections

from misc import main_subtask
from core import *
from table import *

def task_convert_airport(args):
    filename = "../local/input/airport_v2.json"
    filename = file2abspath(filename, __file__)
    map_id_item = file2json(filename)
    map_key = [
        {"name":"iataCode", "alternateName":["3code"]},
        {"name":"icaoCode", "alternateName":["4code"]},
        {"name":"identifier", "alternateName":["id"]},
        {"name":"timezone", "alternateName":["Timezone"]},
        {"name":"name"},
        {"name":"zh_airport"},
    ]

    items = []
    for xid in sorted(map_id_item):
        item = map_id_item[xid]
        item_new = json_dict_copy(item, map_key)
        item_new["@type"] = ["Airport", "CivicStructure", "Place", "Thing"]
        item_new["@id"] = any2sha1(xid)
        item_new["geo"] = {
            "@type": ["GeoCoordinates", "Thing"],
            "altitude": item["Altitude"],
            "latitude": item["Latitude"],
            "longitude": item["Longitude"],
        }
        item_new["address"] = {
            "@type": ["PostalAddress", "Thing"],
            "city": item["Altitude"],
            "addressCountry": item["country"],
        }
        p = "zh_city"
        if p in item:
            item_new["address"]["cityZh"] = item[p]
        p = "zh_region"
        if p in item:
            item_new["address"]["regionZh"] = item[p]
        if item["3code"] == "PEK":
            logging.info(json.dumps(item_new, ensure_ascii=False))
        items.append(item_new)
    
    filename = "../local/output/airport_cnschema.json"
    filename = file2abspath(filename, __file__)
    output = {
      "@context": {
        "@vocab": "http://cnschema.org/"
      },
      "@graph": items
     }
    json2file( output, filename)

if __name__ == "__main__":
    logging.basicConfig(format='[%(levelname)s][%(asctime)s][%(module)s][%(funcName)s][%(lineno)s] %(message)s', level=logging.DEBUG)  # noqa
    logging.getLogger("requests").setLevel(logging.WARNING)

    main_subtask(__name__)

"""
    python cdata/cns_gen.py task_convert_airport

"""

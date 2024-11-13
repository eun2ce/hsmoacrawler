import json
from pprint import pprint

import elasticsearch
from elasticsearch import helpers

index_name = "scrapy"
host = ["http://elasticsearch:9200"]

es = elasticsearch.Elasticsearch(hosts=host)

es.indices.create(index=index_name, body={
    "mappings": {
        "properties": {
            "imageHashes": {
                "type": "dense_vector",
                "dims": 128
            },
            "imageUrl": {
                "type": "text"
            },
            "price": {
                "type": "text"
            },
            "name": {
                "type": "text"
            },
            "site": {
                "type": "text"
            }
        }
    }
}, ignore=400)

pprint(es.indices.get(index=index_name))

data_path = "data/demo_data.json"

with open(data_path, "r", encoding="utf-8") as f:
    data = json.loads(f.read())
result = []
for item in [_f for _f in data if _f]:
    source = item
    image_hashes = source["imageHashes"]
    source["imageHashes"] = [float(i) for i in image_hashes]
    print(len(image_hashes))
    body = {"_index": index_name,
            "_source": source}
    result.append(body)
helpers.bulk(es, result)

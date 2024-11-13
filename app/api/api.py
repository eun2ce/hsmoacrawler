import os

import cv2
import elasticsearch
import requests
import numpy as np

from ..utils.lshash import RandomProjectionHasher


def search(url: str):
    temp_img_path = "temp.jpg"
    with open(temp_img_path, "wb") as f:
        f.write(requests.get(url).content)

    src = cv2.imread(temp_img_path, None)
    gray = cv2.cvtColor(src, cv2.IMREAD_GRAYSCALE)
    feature = cv2.SIFT_create(128)

    keypoints, des = feature.detectAndCompute(gray, None)
    coords = np.array([k.pt for k in keypoints])
    image_hashes = RandomProjectionHasher(8,2).hash_bulk(coords)

    os.remove(temp_img_path)

    es = elasticsearch.Elasticsearch(hosts=["http://elasticsearch:9200"])
    response = es.search(
        index="scrapy",
        filter_path="hits.hits",
        query={
            "knn": {
                "query_vector": image_hashes,
                "field": "imageHashes"
            }
        },
    )
    return response
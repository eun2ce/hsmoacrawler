import json
import logging
import os

import cv2
import numpy as np
from scrapy.utils.project import get_project_settings

from .utils.lshash import RandomProjectionHasher


class ImagePipeline(object):
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.settings = get_project_settings()

        data_dir = self.settings.get("DATA_DIR")
        demo_file_name = self.settings.get("DEMO_FILE")
        self.demo_file_path = os.path.join(data_dir, demo_file_name)
        self.result = []

    def close_spider(self, spider):
        print("################################################")
        print("in?")
        print("################################################")

        self.export_json(self.result)

    def process_item(self, item, spider):
        image_file_path = item["imageHashes"][0]  # 임시로 저장 된 file path 값 파싱.

        checked = (None, None, None)
        keypoints, des, coords = self.compute_coordinates(image_file_path) or checked

        if coords is not None:
            item["imageHashes"] = self.create_image_hashes(coords)
        else:
            # TODO .. 이미지 로드에 실패 해서 분석이 어려운 경우
            pass

        self.result.append(dict(item))
        return item

    def export_json(self, item):
        with open(self.demo_file_path, "w", encoding="utf-8") as f:
            json.dump(item, f, ensure_ascii=False)
        return item

    def compute_coordinates(self, file_path):
        # 불러오기
        src = cv2.imread(file_path, None)
        if src is None:
            self.logger.debug(f"Unable to load image. file path: {file_path}")
            return None

        gray = cv2.cvtColor(src, cv2.IMREAD_GRAYSCALE)

        # 특정 알고리즘 객체 생성
        feature = cv2.SIFT_create(128)
        # 특징점 검출 및 기술자 계산
        keypoints, des = feature.detectAndCompute(gray, None)
        coords = np.array([k.pt for k in keypoints])

        return keypoints, des, coords

    def create_image_hashes(self, coords, hash_size=8, input_dim=2):
        # 해시 생성
        return RandomProjectionHasher(hash_size, input_dim).hash_bulk(coords)

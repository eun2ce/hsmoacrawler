# moacrawler

hsmoa.com 상품 정보를 크롤링하여 이미지 검색 엔 및 데모 웹 페이지를 제공합니다.

## 이미지 검색 동작 원리

이미지에서 SIFT를 추출하고 LSHash로 해싱하여, 해당 결과를 ES에 저장해 상품을 검색할 수 있도록 합니다.

자세한 내용은 아래와 같습니다.

1. SIFT 알고리즘으로 이미지의 크기가 달라지고, 회전하더라도 같은 곳에서 특징점을 찾아냅니다.
2. 해당 이미지에서 특징점이 찾아지면, LSHash를 사용해 특징점을 해시 테이블에 저장하고 빠르게 비교하여 찾아낼 수 있도록 결과물파일에 저장합니다.
3. 데이터는 ES 에 적재하여 동일한 상품을 검색합니다.

## 시작하기

```shell
$ docker-compose up -d
```

## crawl

* selenium을 기반으로 웹 사이트에 방문하여 크롤링합니다.
* 수집 된 페이지 소스 파일로부터 bs4와 scrapy를 이용해 데이터를 가공합니다.
* 가공 된 데이터는 원하는 형태의 파일로 저장됩니다.

```shell
$ conda create -n moacrawler python=3.11
$ conda activate moacrawler
$ pip install -r requirements.txt
$ cd scraper
$ scrapy crawl moa_spider
$ scrapy crawl image_download_spider
```

## search

- 저장 된 데이터를 기반으로 es에 저장하고 검색할 수 있습니다.

```shell
$ docker-compose up -d
$ curl -X 'GET' \
  'http://localhost:8080/search/?url=https%3A%2F%2Fhsmoa.com%2F_next%2Fimage%3Furl%3Dhttps%253A%252F%252Fthum.buzzni.com%252Funsafe%252F360x0%252Fcenter%252Fhttp%253A%252F%252Fcdn.image.buzzni.com%252F2024%252F10%252F07%252Fsa7Z644g.jpg%26w%3D640%26q%3D75' \
  -H 'accept: application/json'
```

필요 시 http://localhost:8080/docs#/default/search_search__get 에서도 결과를 조회 해 볼 수 있습니다.
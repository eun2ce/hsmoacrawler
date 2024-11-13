FROM python:3.11
WORKDIR /

RUN apt-get -y update && \
    apt install wget && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt -y install ./google-chrome-stable_current_amd64.deb   # Google Chrome 다운로드 및 설치

COPY * /.
RUN pip install --no-cache-dir -r requirements.txt  # 패키지 의존성 설치

WORKDIR /scraper
CMD ["scrapy", "crawl", "moa_spider"]
CMD ["scrapy", "crawl", "image_download_spider"]

WORKDIR /
CMD ["python", "/app/pre_action.py"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
from fastapi import FastAPI

from app.api import api

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Fast API in Python"}


@app.get("/search/")
def search(url: str):
    print(url)
    return api.search(url)

import os

import databases
from fastapi import FastAPI
from elasticsearch import AsyncElasticsearch

DATABASE_URL = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DB']}"
STATUS_OK = {"success": True}

app = FastAPI()

es = AsyncElasticsearch(f"http://{os.environ['ELASTIC_HOST']}:{os.environ['ELASTIC_PORT']}")
database = databases.Database(DATABASE_URL)


@app.on_event("startup")
async def startup():
    await database.connect()

    if not (await es.indices.exists(index="fastapi")):
        await es.indices.create(index="fastapi")


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

    await es.close()


@app.get("/")
async def root():
    print(await database.fetch_all("SELECT 1+2"))
    print(await es.search(
        index="fastapi", body={"query": {"multi_match": {"query": "random query"}}}
    ))
    return STATUS_OK

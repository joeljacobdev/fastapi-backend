from elasticsearch import AsyncElasticsearch

es = AsyncElasticsearch(hosts=['0.0.0.0'])


async def setup():
    # setup connections
    # update mapping
    return es


async def cleanup():
    await es.close()

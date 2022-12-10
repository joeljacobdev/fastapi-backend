from elasticsearch import AsyncElasticsearch

es = None


async def setup(config):
    # setup connections
    # update mapping
    es = AsyncElasticsearch(hosts=config['hosts'])
    return es


async def cleanup():
    await es.close()

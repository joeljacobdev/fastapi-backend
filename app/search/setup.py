from elasticsearch import AsyncElasticsearch
import app.search as search_app


async def setup(config):
    # setup connections
    # update mapping
    search_app.es_client = AsyncElasticsearch(hosts=config['hosts'])
    return search_app.es_client


async def cleanup():
    await search_app.es_client.close()

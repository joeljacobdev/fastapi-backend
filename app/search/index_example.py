from elasticsearch import helpers
from faker import Faker
from faker.providers import date_time, lorem, person

from app.search import es_client

fake = Faker()
fake.add_provider(lorem)
fake.add_provider(date_time)
fake.add_provider(person)

post_index_mapping = {
    "post_id": {
        "type": "integer"
    },
    "title": {
        "type": "text"
    },
    "description": {
        "type": "text",
        "index": False
    },
    "creator_name": {
        "type": "keyword"
    },
    "creator_email": {
        "type": "keyword"
    },
    "tags": {
        "type": "keyword"
    },
    "created_at": {
        "type": "date"
    }
}
# https://medium.com/driven-by-code/elasticsearch-global-ordinals-31df2806391f
# https://www.factweavers.com/blog/join-in-elasticsearch/
# TODO play with eager_global_ordinals
post_shared_with_mapping = {
    "post_id": {
        "type": "integer"
    },
    "up_voted_users": {
        "type": "keyword"
    },
    "down_voted_users": {
        "type": "keyword"
    },
    "commented_users": {
        "type": "keyword"
    }
}
idx1 = await es_client.indices.create(
    index="posts",
    mappings={
        "properties": {
            **post_index_mapping,
            **post_shared_with_mapping,
        }
    },
    settings={
        "number_of_shards": 3,
        "number_of_replicas": 2
    }
)
posts = []
for i in range(1001, 1101):
    posts.append({
        '_op_type': 'create',
        '_id': i,
        '_routing': i % 3,
        '_index': "posts",
        '_source': {
            'post_id': i,
            'title': fake.sentence(nb_words=10),
            'description': fake.text(),
            'creator_name': fake.name(),
            'creator_email': fake.email(),
            'tags': fake.words(),
            'created_at': fake.date_time_between(),
            'shared_criteria': {
                'name': 'posts'
            }
        }
    })
await helpers.async_bulk(es_client, posts)

post_shared = []
for i in range(1001, 1101):
    post_shared.append({
        '_op_type': 'create',
        '_id': f'post_shared.{i}',
        '_routing': i % 3,
        '_index': "posts",
        '_source': {
            'up_voted_users': [fake.email() for _ in range(100)],
            'down_voted_users': [fake.email() for _ in range(100)],
            'commented_users': [fake.email() for _ in range(1000)],
            'shared_criteria': {
                'name': 'posts_shared_with',
                'parent': i
            }
        }
    })
await helpers.async_bulk(es_client, post_shared)

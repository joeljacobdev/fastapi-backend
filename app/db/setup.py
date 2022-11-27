from tortoise import Tortoise, connections


async def init_db(config):
    await Tortoise.init(config=config)


async def cleanup():
    connections.close_all(discard=True)

from tortoise import Tortoise, connections


async def setup(config):
    await Tortoise.init(config=config)


async def cleanup():
    await connections.close_all(discard=True)

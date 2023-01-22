"""
Everything imported and defined in this file will be available in the shell.

We use ptpython instead of ipython because ipython doesnt really have any good
ways to being embedded the way we want.
"""

import asyncio

from ptpython.repl import embed

from main import on_startup, on_shutdown

loop = asyncio.get_event_loop()


async def setup():
    await on_startup()
    try:
        await embed(globals=globals(), return_asyncio_coroutine=True, patch_stdout=True)
    except EOFError:
        loop.stop()


def main():
    asyncio.ensure_future(setup())
    loop.run_forever()
    on_shutdown()
    loop.close()


if __name__ == "__main__":
    main()

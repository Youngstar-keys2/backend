import asyncio

from app.db.db import DB
from app.queries.tags import load_tags


async def main():
    await DB.connect_db()
    await load_tags()
    await DB.disconnect_db()

asyncio.get_event_loop().run_until_complete(main())
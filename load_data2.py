import asyncio

from yaml import load

from app.db.db import DB
from app.queries.dataset import load_dataset




async def main():
    await DB.connect_db()
    await load_dataset()
    await DB.disconnect_db()

asyncio.get_event_loop().run_until_complete(main())
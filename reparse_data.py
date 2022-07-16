import asyncio
from app.db.db import DB


async def main():
    await DB.connect_db()
    categories = [
        "country_code",
        "place",
        "statee",
        "province",
        "community",
    ]
    for offset in range(0, 1600000, 10000):
        sql = """select id,country_code,zip_code,place,statee,province,community,latitude,longtitude from country
                limit 10000 offset $1"""
        items = await DB.con.fetch(sql, offset)
        for item in items:
            for category in categories:
                sql = """select id from categories where name = $1"""
                idd = await DB.con.fetchval(sql, category)
                sql = """insert into categories_subcategories (category_id, subcategory_name)
                         values ($1, $2)"""
                await DB.con.execute(sql, idd, item[category])
                sql = """update subcategories set parent_category=$1 where name = $2"""
                await DB.con.execute(sql, idd, item[category])
    await DB.disconnect_db()

asyncio.get_event_loop().run_until_complete(main())

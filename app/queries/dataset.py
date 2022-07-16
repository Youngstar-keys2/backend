from app.db.db import DB


# codes text,
#     reglaments text,
#     group text,
#     name text,
#     il text,
#     applicant text,
#     address_applicant text,
#     maker text,
#     country text,
#     address_maker text

# TODO Чекнуть то что в подкатегории могут быть заданы списком
# TODO Россия вру


async def load_dataset():
    async def get_category_if_present(subcategory: str) -> str | None:
        sql = """select c.name from categories as c join subcategories as sc
                 on c.id = sc.parent_category
                 where sc.name = $1"""
        return await DB.fetchval(sql, subcategory)

    categories = [
        "id",
        "codes",
        "reglament",
        "name",
        "il",
        "applicant",
        "address_applicant",
        "maker",
        "country",
        "address_maker",
    ]
    for offset in range(0, 66755, 1000):
        sql = """select * from dataset limit 1000 offset $1"""
        items = await DB.con.fetch(sql, offset)
        for item in items:
            categories = dict()
            hernya = item["address_maker"]
            words = hernya.split(" ")
            prev = 0
            for i in range(prev, len(words)):
                query = " ".join(words[prev:i])
                if query == "РОССИЯ":
                    query = "RU"
                category = await get_category_if_present(query)
                if category:
                    categories[query] = category
                    prev = i

    for category in categories:
        k = 0
        sql = f"""select distinct({category})  from dataset"""
        tags = await DB.con.fetch(sql)
        if category == "codes":
            tags = [list(filter(lambda x: x, x[category].split(";"))) for x in tags]
            tags = sum(tags, [])
        elif category == "id":
            tags = [x[category].split()[0] for x in tags]
        else:
            tags = [x[category] for x in tags]
        sql = """insert into data_categories(name) values ($1) on conflict do nothing RETURNING id"""
        idk = await DB.con.fetchval(sql, category)
        for link in tags:
            print(k)
            if not link:
                continue
            sql = """insert into data_subcategories(name,parent_category ) values ($1,$2) on conflict do nothing"""
            await DB.con.execute(sql, link, idk)
            sql = (
                f""" select id,latitude ,longtitude from dataset where {category}=$1"""
            )
            info = await DB.con.fetch(sql, link)
            for itemsk in info:
                sql = "insert into data (latitude, longtitude) values ($1,$2) returning id"
                id = await DB.con.fetchval(
                    sql, itemsk["latitude"], itemsk["longtitude"]
                )
                sql = "insert into data_data_subcategories(item_id, name_sub) values ($1,$2) on conflict do nothing"
                await DB.con.execute(sql, id, link)
                k += 1


async def get_data_info(data_id: int):
    sql = """select ds.name, c.name from data_subcategories as ds join data_data_subcategories as dds
             on dds.name = ds.name join data_categories as c on c.id = ds.parent_category_id
             where dds.data_id = $1"""
    return await DB.con.fetch(sql, data_id)


# async def seek_data_info(seek: list, last_page: int):
#     sql = """select items.id,items.latitude,items.longtitude  from subcategories as sub JOIN items_subcategories as isub
#                  on sub.name = isub.name_sub JOIN items on isub.item_id = items.id where sub.name = ANY($1::text[]) limit $2 offset $3"""
#     sql = """with ids as
#              (select items.id as iid, count(isub.name_sub) as cnt
#                from items join items_subcategories as isub
#                on items.id = isub.item_id
#                where isub.name_sub = ANY($1::text[])
#                group by items.id)
#              select items.id, items.latitude, items.longtitude, cnt from items
#              join ids on ids.iid = items.id
#              where cnt = $4
#              limit $2
#              offset $3"""
#     tags = await DB.con.fetch(sql, seek, 30, last_page, len(seek))
#     return tags


async def get_data(category: str):
    sql = """select s.name from data_subcategories as s join data_categories as c on  s.parent_category = c.id where c.name = $1"""
    return await DB.con.fetch(sql, category)

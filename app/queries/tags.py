from app.db.db import DB


# async def load_tags():
#     categories = [
#         "country_code",
#         "place",
#         "statee",
#         "province",
#         "community",
#     ]
#     sql = """
#         truncate table items cascade
#     """
#     await DB.con.execute(sql)
#     sql = """truncate table subcategories cascade"""
#     await DB.con.execute(sql)
#     sql = """truncate table categories cascade"""
#     await DB.con.execute(sql)

#     for category in categories:
#         k = 0
#         sql = f"""select distinct({category})  from country"""
#         tags = await DB.con.fetch(sql)
#         tags = [x[category] for x in tags]
#         sql = """insert into categories(name) values ($1) on conflict do nothing RETURNING id"""
#         idk = await DB.con.fetchval(sql, category)
#         for link in tags:
#             print(k)
#             if not link:
#                 continue
#             sql = """insert into subcategories(name,parent_category ) values ($1,$2) on conflict do nothing"""
#             await DB.con.execute(sql, link, idk)
#             sql = (
#                 f""" select id,latitude ,longtitude from country where {category}=$1"""
#             )
#             info = await DB.con.fetch(sql, link)
#             for itemsk in info:
#                 sql = "insert into items (latitude, longtitude) values ($1,$2) returning id"
#                 id = await DB.con.fetchval(
#                     sql, itemsk["latitude"], itemsk["longtitude"]
#                 )
#                 sql = "insert into items_subcategories(item_id, name_sub) values ($1,$2) on conflict do nothing"
#                 await DB.con.execute(sql, id, link)
#                 k += 1


async def load_tags():
    categories = [
        "country_code",
        "place",
        "statee",
        "province",
        "community",
    ]
    sql = """
        truncate table items cascade
    """
    # await DB.con.execute(sql)
    sql = """truncate table subcategories cascade"""
    # await DB.con.execute(sql)
    sql = """truncate table categories cascade"""
    # await DB.con.execute(sql)
    ids = dict()
    for category in categories:
        sql = """insert into categories(name) values ($1) on conflict do nothing RETURNING id"""
        temp_id = await DB.con.fetchval(sql, category)
        ids[category] = temp_id
    for offset in range(0, 1548347, 1000):
        sql = """select id,country_code,zip_code,place,statee,province,community,latitude,longtitude from country
                limit 1000 offset $1"""
        items = await DB.con.fetch(sql, offset)
        for item in items:
            sql = """insert into items(id,latitude,longtitude) values ($1,$2,$3) on conflict do nothing returning id"""
            idd = await DB.con.fetchval(
                sql, item["id"], item["latitude"], item["longtitude"]
            )
            if not idd:
                continue
            for category in categories:
                if not item[category]:
                    continue
                sql = """insert into subcategories(name,parent_category) values ($1,$2) on conflict do nothing"""
                await DB.con.execute(sql, item[category], ids[category])
                sql = """insert into items_subcategories(item_id,name_sub) values ($1,$2) on conflict do nothing"""
                await DB.con.execute(sql, item["id"], item[category])


async def seek_tags_info(seek: list, last_page: int):
    sql = """select items.id,items.latitude,items.longtitude  from subcategories as sub JOIN items_subcategories as isub
                 on sub.name = isub.name_sub JOIN items on isub.item_id = items.id where sub.name = ANY($1::text[]) limit $2 offset $3"""
    sql = """with ids as
             (select items.id as iid, count(isub.name_sub) as cnt
               from items join items_subcategories as isub
               on items.id = isub.item_id
               where isub.name_sub = ANY($1::text[])
               group by items.id)
             select items.id, items.latitude, items.longtitude, cnt from items
             join ids on ids.iid = items.id
             where cnt = $4
             limit $2
             offset $3"""
    tags = await DB.con.fetch(sql, seek, 20, last_page, len(seek))
    l = []
    for items in tags:
        sql = """
            select distinct(iss.name_sub) from items as i 
            join items_subcategories as iss
            on i.id = iss.item_id
            join categories_subcategories cs 
            on cs.subcategory_name = iss.name_sub 
            where cs.category_id = 56 and i.id = $1
        """
        # sql = """select distinct(iss.name_sub) from items_subcategories as iss
        #          join items as i
        #          on iss.item_id = i.id
        #          join items_subcategories as iss2
        #          on i.id = iss2.item_id
        #          join categories_subcategories as cs 
        #          on cs.subcategory_name = iss2.name_sub
        #         where i.id=$1 and cs.category_id = 56 limit 20 offset 1"""
        name = await DB.con.fetch(sql, items["id"])
        l.append({"id":items["id"], "latitude": items["latitude"],"longtitude": items["longtitude"],"izgot":[dict(**x) for x in name] })
    return l


async def get_tags(category: str, page: int):
    sql = """select s.name from subcategories as s
             join categories_subcategories as cs
             on cs.subcategory_name = s.name
             join categories as c
             on c.id = cs.category_id
             where c.name = $1
             limit $2 offset $3"""
    return await DB.con.fetch(sql, category, 100, page)


async def get_product_sql(name: str):
    sql = """  """
    

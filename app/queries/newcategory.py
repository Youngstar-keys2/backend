

from app.models import Newcategory
from app.db.db import DB


async def get_category_if_present(subcategory: str) -> str :
    sql = """select c.name from categories as c join subcategories as sc
                on c.id = sc.parent_category
                where sc.name = $1"""
    return await DB.con.fetchval(sql, subcategory)


async def add_new_category(cat: Newcategory):
    categories = dict()
    hernya = cat.addres_izgot
    words = hernya.split(" ")
    prev = 0
    for i in range(prev, len(words)):
        query = " ".join(words[prev:i])
        if query == 'РОССИЯ':
            query = 'RU'
        category = await get_category_if_present(query)
        if category and query not in categories.keys():
            categories[query] = category
            prev = i
    sql = """with ids as 
            (select items.id as p, count(iss.name_sub) as cnt from items
            join items_subcategories as iss
            on iss.item_id = items.id
            where iss.name_sub = ANY($1::text[])
            group by p)

            select id from items join ids
            on items.id = ids.p
            where ids.cnt = $2"""
    result = await DB.con.fetchval(sql, categories.keys(), len(categories.keys()))
    print(result)
    if not result:
        print(categories.keys(), result, query)
        return
    topic = [
        "codes",
        "reglament",
        "groups", 
        "name",
        "il",
        "applicant",
        "address_applicant",
        "maker",
        "country",
        "address_maker",
    ]
    l = [cat.code, cat.tex_regl, cat.group, cat.name, cat.il, cat.applicant, cat.addres_applicant,cat.izgotovitel ,cat.country]
    for i in range( len(topics)):
        sql = """insert into categories(name) values ($1) on conflict do nothing"""
        await DB.con.execute(sql, topic[i])
        sql = """select id from categories where name = $1"""
        category = await DB.con.fetchval(sql, topic[i])
        sql = (
            """insert into subcategories(name) values ($1) on conflict do nothing"""
        )
        print(category, result, str(l[i]))
        await DB.con.execute(sql, str(l[i]))
        sql = """insert into categories_subcategories(category_id, subcategory_name)
                    values ($1, $2) on conflict do nothing"""
        await DB.con.execute(sql, category, str(l[i]))
        sql = """insert into items_subcategories(item_id, name_sub)
                    values ($1, $2) on conflict do nothing"""
        await DB.con.execute(sql, result, str(l[i]))

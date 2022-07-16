from app.db.db import DB
from dask import dataframe as dd
import numpy


async def get_category_if_present(subcategory: str) -> str | None:
    sql = """select c.name from categories as c join subcategories as sc
                on c.id = sc.parent_category
                where sc.name = $1"""
    return await DB.fetchval(sql, subcategory)


async def main():
    df = dd.read_csv("D:/backend/dataset.csv")
    d = numpy.array(df)
    l = []
    for i in d:
        for j in i:
            l.append(j)

        categories = dict()
        hernya = l[11]
        words = hernya.split(" ")
        prev = 0
        for i in range(prev, len(words)):
            query = " ".join(words[prev:i])
            category = await get_category_if_present(query)
            if category:
                categories[query] = category
                prev = i
        sql = """with ids as 
                (select items.id as p, count(iss.name) as cnt from items
                join items_subcategories as iss
                on iss.item_id = items.id
                where iss.name_sub = ANY($1::text[]))

                select id from items join ids
                on items.id = ids.p
                where ids.cnt = $2"""
        result = await DB.con.fetchval(sql, categories.keys(), len(categories.keys()))
        l[11] = result
        if not result:
            print(categories.keys(), result)
            continue
        topic = [
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
        for i in range(1, 11):
            sql = """insert into categories(name) values ($1) on conflict do nothing"""
            await DB.con.execute(sql, topic[i])
            sql = (
                """insert into subcategories(name) values ($1) on conflict do nothing"""
            )
            await DB.con.execute(sql, l[i])
            sql = """insert into items_subcategories(item_id, name_sub)
                     values ($1, $2)"""
            await DB.con.execute(sql, result, l[i])
    l.clear()

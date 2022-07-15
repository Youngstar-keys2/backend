from dask import dataframe as dd
import os
import numpy
import asyncio
import asyncpg

from dotenv import load_dotenv

load_dotenv("local.env")

DATABASE_URL: str = os.environ["DATABASE_URL"]

sql = """ INSERT INTO country(country_code, zip_code,place,statee,state_code,province,province_code,community,community_code,latitude, longtitude)
           VALUES($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11)"""


async def main():
    conn = await asyncpg.connect(DATABASE_URL)
    for filename in os.listdir("csv"):
        df = dd.read_csv(
            f"csv/{filename}",
            dtype={
                "state_code": object,
                "province_code": object,
                "community": object,
                "province": object,
                "community_code": object,
                "zipcode": object,
            },
        )
        d = numpy.array(df)
        l = []
        for i in d:
            k = 0
            for j in i:
               
                if j != j:
                    l.append(None)
                else:
                    l.append(j)
            await conn.execute(sql,l[0],l[1],l[2],l[3],l[4],l[5],l[6],l[7],l[8],l[9],l[10])
            l.clear()
asyncio.get_event_loop().run_until_complete(main())

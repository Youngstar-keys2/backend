import hashlib
import json
from app.db.db import DB
from app.exceptions import InternalServerError
from app.settings import REDIS_PORT, REDIS_HOSTNAME
import aioredis

from app.utils.formatter import format_records


class Redis:

    con: aioredis.Redis = None

    @classmethod
    async def connect_redis(cls) -> None:
        cls.con = None
        try:
            cls.con = aioredis.from_url(
                f"redis://:@{REDIS_HOSTNAME}:{REDIS_PORT}",
                encoding="utf-8",
                decode_responses=True,
            )
        except Exception as error:
            raise InternalServerError() from error

    @classmethod
    async def disconnect_redis(cls) -> None:
        if cls.con:
            await cls.con.close()

    @classmethod
    async def load_tags(cls) -> None:
        if not cls.con:
            return
        await cls.con.flushall()
        categories = [
            "country_code",
            "place",
            "statee",
            "province",
            "community",
        ]  # TODO отдать ктаегории фронту
        for category in categories:
            sql = f"""select distinct({category})  from country"""
            tags = await DB.con.fetch(sql)
            tags = [x[category] for x in tags]
            for link in tags:
                await cls.con.lpush(category, link)
                sql = f""" select id,latitude ,longtitude from country where {category}=$1"""
                info = await DB.con.fetch(sql, link)
                for itemsk in info:
                    await cls.con.zadd(
                        f"{category}_" + link,
                        {
                            str(itemsk["latitude"])
                            + ","
                            + str(itemsk["longtitude"]): itemsk["id"]
                        },
                    )

    @classmethod
    async def seek_tags_info(cls, seek: dict[tuple], last_page: int):
        key = list(seek.keys())[0]
        data = seek[key][0]
        hashed = hashlib.sha224(json.dumps(seek, sort_keys=True)).hexdigest()
        spisok = [key + "_" + item for item in data]
        await cls.con.zinterstore(hashed, len(spisok), spisok)
        tags = await cls.con.zrange(hashed, last_page, last_page + 30)
        await cls.con.delete(hashed)
        return tags

    @classmethod
    async def get_tag(cls, category):
        return await cls.con.lrange(category, 0, -1)

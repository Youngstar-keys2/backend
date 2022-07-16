from asyncpg import Record

from app.db.db import DB


async def check_auth(login: str) -> Record:
    sql = """   SELECT id,name,password
                FROM users
                WHERE name = $1;"""
    return await DB.con.fetchrow(sql, login)


async def create_user(
    applicant: str,
    addres_applicant: str,
    country: str,
    login: str,
    password: str,
    il: str,
) -> None:
    sql = """  INSERT INTO users (name, password, applicant,addres_applicant,country,il)
                VALUES ($1,$2,$3,$4,$5,$6);"""
    await DB.con.execute(sql, login, password, applicant, addres_applicant, country, il)

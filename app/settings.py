import os

from dotenv import load_dotenv

load_dotenv("local.env")

DATABASE_URL: str = os.environ["DATABASE_URL"]
SECRET_KEY: str = os.getenv("SECRET_KEY")
ALGORITHM: str = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REDIS_HOSTNAME: str = os.getenv("REDIS_HOSTNAME")
REDIS_PORT: str = os.getenv("REDIS_PORT")

import os
from dotenv import load_dotenv

load_dotenv()

IP = os.getenv("ip")

PGUSER = os.getenv('pguser')

PGPASSWORD = os.getenv('pgpassword')

DATABASE = os.getenv("database")

POSTGRES_URI = f'postgresql://{PGUSER}:{PGPASSWORD}@{IP}/{DATABASE}'

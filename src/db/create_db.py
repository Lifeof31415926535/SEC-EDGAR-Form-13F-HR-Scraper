import psycopg2

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import sql
from psycopg2.errors import DuplicateDatabase

from src.config import DB_CONFIG


class DbCreator:
    def __init__(
            self,
            db_name=DB_CONFIG['name'],
            db_user=DB_CONFIG['user'],
            db_user_password=DB_CONFIG['password'],
            db_host=DB_CONFIG['host'],
            db_port=DB_CONFIG['port'],
    ):
        self.connected = False
        self.db_name = db_name
        self.db_user = db_user
        self.db_user_password = db_user_password
        self.db_host = db_host
        self.db_port = db_port

        try:
            self.conn = psycopg2.connect(
                dbname='postgres',
                user='postgres',
                password='Pass123!',
                host='localhost',
                port=DB_CONFIG['port']
            )
            self.connected = True
        except Exception as exc:
            print(exc)
            print("Failed to establish connection.")

    def __del__(self):
        if self.connected:
            self.conn.close()

    def create_db_user(self):
        if not self.connected:
            return

        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = self.conn.cursor()

        cur.execute(f"SELECT * FROM pg_user WHERE usename = '{self.db_user}';")
        if cur.fetchone() is None:
            cur.execute(
                f"CREATE USER {self.db_user} WITH PASSWORD '{self.db_user_password}';"
            )
        self.conn.commit()

    def create_db(self):
        if not self.connected:
            return

        cur = self.conn.cursor()

        try:
            cur.execute(
                f"CREATE DATABASE {self.db_name} WITH OWNER {self.db_user};"
            )
            self.conn.commit()
        except DuplicateDatabase:
            pass

    def grant_privileges(self):
        if not self.connected:
            return

        cur = self.conn.cursor()
        cur.execute(
            f"GRANT ALL PRIVILEGES ON DATABASE {self.db_name} TO {self.db_user};"
        )
        self.conn.commit()

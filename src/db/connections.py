import psycopg2

from config import DB_CONFIG


class ConnectionManager:
    def __init__(self, profile: dict):
        self.profile = profile

    def __enter__(self):
        print(f"Opening connection to database {self.profile['name']}.")
        self.connection = psycopg2.connect(
            dbname=self.profile['name'],
            user=self.profile['user'],
            password=self.profile['password'],
            host=self.profile['host'],
            port=self.profile['port']
        )
        print(f"Connection established. ")
        print(f"Creating cursor.")
        self.cursor = self.connection.cursor()
        print("Cursor created.")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.connection.close()
        print(f"Connection to database {self.profile['name']} closed.")

    def commit(self):
        self.connection.commit()


def connection_manager(profile=DB_CONFIG) -> ConnectionManager:
    return ConnectionManager(profile)

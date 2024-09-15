import pymongo
import psycopg2
from psycopg2 import sql
from settingsmanager.SettingsManager import SettingsManager

class DatabaseManager:
    def __init__(self):
        self.mongo_client = None
        self.postgres_conn = None
        self._connect_mongodb()
        self._connect_postgresql()

    def _connect_mongodb(self):
        """
        Establishes a connection to the MongoDB database.
        """
        settings = SettingsManager.get_settings()
        mongo_uri = settings.get('mongodb_uri')
        mongo_db_name = settings.get('mongodb_db_name')
        
        try:
            self.mongo_client = pymongo.MongoClient(mongo_uri)
            self.mongo_db = self.mongo_client[mongo_db_name]
            self.mongo_collection = self.mongo_db['jobs']
            print("Connected to MongoDB successfully.")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")

    def _connect_postgresql(self):
        """
        Establishes a connection to the PostgreSQL database.
        """
        settings = SettingsManager.get_settings()
        pg_conn_params = {
            'dbname': settings.get('postgres_db_name'),
            'user': settings.get('postgres_user'),
            'password': settings.get('postgres_password'),
            'host': settings.get('postgres_host'),
            'port': settings.get('postgres_port')
        }

        try:
            self.postgres_conn = psycopg2.connect(**pg_conn_params)
            self.postgres_cursor = self.postgres_conn.cursor()
            print("Connected to PostgreSQL successfully.")
        except Exception as e:
            print(f"Error connecting to PostgreSQL: {e}")

    def is_url_in_mongodb(self, url):
        """
        Checks if a URL exists in the MongoDB collection.
        """
        try:
            result = self.mongo_collection.find_one({'url': url})
            return result is not None
        except Exception as e:
            print(f"Error checking URL in MongoDB: {e}")
            return False

    def add_url_to_mongodb(self, url):
        """
        Adds a URL to the MongoDB collection.
        """
        try:
            self.mongo_collection.insert_one({'url': url})
            print(f"URL added to MongoDB: {url}")
        except Exception as e:
            print(f"Error adding URL to MongoDB: {e}")

    def is_url_in_postgresql(self, url):
        """
        Checks if a URL exists in the PostgreSQL database.
        """
        query = sql.SQL("SELECT EXISTS (SELECT 1 FROM jobs WHERE url = %s)")
        try:
            self.postgres_cursor.execute(query, (url,))
            return self.postgres_cursor.fetchone()[0]
        except Exception as e:
            print(f"Error checking URL in PostgreSQL: {e}")
            return False

    def add_url_to_postgresql(self, url):
        """
        Adds a URL to the PostgreSQL database.
        """
        query = sql.SQL("INSERT INTO jobs (url) VALUES (%s) ON CONFLICT DO NOTHING")
        try:
            self.postgres_cursor.execute(query, (url,))
            self.postgres_conn.commit()
            print(f"URL added to PostgreSQL: {url}")
        except Exception as e:
            print(f"Error adding URL to PostgreSQL: {e}")
            self.postgres_conn.rollback()

    def close_connections(self):
        """
        Closes the connections to both MongoDB and PostgreSQL.
        """
        if self.mongo_client:
            self.mongo_client.close()
            print("MongoDB connection closed.")

        if self.postgres_conn:
            self.postgres_cursor.close()
            self.postgres_conn.close()
            print("PostgreSQL connection closed.")

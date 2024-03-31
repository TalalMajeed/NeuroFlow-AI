from NeuroFlow.server import app
import psycopg2
import os

try:
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        database='verceldb',
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
except Exception as e:
    print(f"Error connecting to database: {e}")
    conn = None
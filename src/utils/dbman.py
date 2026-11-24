import pandas as pd
import psycopg2

# Database connection parameters
db_params = {
    "host": "localhost",
    "database": "fault_detection", 
    "user": "username",
    "password": "password",
    "port": 5432,
}

def extract(query:str):
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        df = pd.read_sql_query(query, conn)
        return df

    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
    finally:
        if conn is not None:
            conn.close()

def create(query: str):
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return True

    except Exception as e:
        print(f"Error while executing query {e}")

def n_create(queries:list):
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cur:
                for query in queries:
                    cur.execute(query)
                return True

    except Exception as e:
        print(f"Error while executing query {e}")
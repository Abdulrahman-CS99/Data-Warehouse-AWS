import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries

def drop_tables(cur, conn):
    """
    Drops existing tables if they exist in Redshift.
    
    Parameters:
        cur: Cursor object to execute PostgreSQL commands.
        conn: Connection to the Redshift database.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()

def create_tables(cur, conn):
    """
    Creates tables in Redshift as per the schema defined in sql_queries.py.
    
    Parameters:
        cur: Cursor object to execute PostgreSQL commands.
        conn: Connection to the Redshift database.
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()

def main():
    """
    - Establishes connection to Redshift.
    - Calls functions to drop existing tables and create new tables.
    - Closes the connection.
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect(
        "host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values())
    )
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()

if __name__ == "__main__":
    main()

import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries

def load_staging_tables(cur, conn):
    """
    Loads data from S3 into staging tables in Redshift using the COPY command.
    
    Parameters:
        cur: Cursor object to execute PostgreSQL commands.
        conn: Connection to the Redshift database.
    """
    print("Loading staging tables...")
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()
    
    print("Staging tables loaded.")

def insert_tables(cur, conn):
    """
    Inserts data from staging tables into fact and dimension tables.
    
    Parameters:
        cur: Cursor object to execute PostgreSQL commands.
        conn: Connection to the Redshift database.
    """
    
    print("Inserting into final tables...")
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()
    
    print("Final tables inserted.")


def main():
    """
    - Establishes connection to Redshift.
    - Calls functions to load staging tables and insert data into analytics tables.
    - Closes the connection.
    """
    
    print("Starting ETL process...")
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect(
        "host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values())
    )
    cur = conn.cursor()

    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()
    print("ETL process completed successfully.")

if __name__ == "__main__":
    main()

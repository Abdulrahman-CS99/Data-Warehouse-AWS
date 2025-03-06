# Data Warehouse with AWS Redshift

## Project Overview
This project builds an ETL pipeline to extract, transform, and load (ETL) data from AWS S3 into Amazon Redshift for Sparkify, a music streaming startup. The pipeline processes JSON log and song metadata to create an optimized star schema database for analytics.

## Purpose of the Database & Analytical Goals
Sparkify data have grown and they need a scalable data warehouse for their advanced analytics team. The goal of this database is to:

- **Track user song plays**: Identify trends in listening behavior.
- **Analyze user engagement**: Determine which users are most active.
- **Understand artist popularity**: Find the most asrtist that have popular songs.
- **Improve business strategy**: Help Sparkify optimize their platform based on user activity insights.

## Dataset
- **Song Dataset**: Contains metadata about songs and artists (extracted from the Million Song Dataset).
- **Log Dataset**: Contains user activity logs for music playback.

## Database Schema (Star Schema)
The database follows a **Star Schema** design which is great for analytical queries due to its denormalized structure. This improves query performance by reducing the need for complex joins.

### Fact Table:
- **`songplays`**: Stores records of song plays (events with `page='NextSong'`).
  - **Columns**: `songplay_id`, `start_time`, `user_id`, `level`, `song_id`, `artist_id`, `session_id`, `location`, `user_agent`

### Dimension Tables:
- **`users`**: Stores user details (`user_id`, `first_name`, `last_name`, `gender`, `level`).
- **`songs`**: Stores song metadata (`song_id`, `title`, `artist_id`, `year`, `duration`).
- **`artists`**: Stores artist metadata (`artist_id`, `name`, `location`, `latitude`, `longitude`).
- **`time`**: Stores timestamps of song plays (`start_time`, `hour`, `day`, `week`, `month`, `year`, `weekday`).

## ETL Pipeline Explanation
The ETL pipeline extracts raw JSON data from S3, transforms it, and loads it into Redshift:

1. **Extract**: Data is copied from **S3** into **staging tables** in Redshift using the `COPY` command.
2. **Transform**: Data is cleaned and structured for analysis.
3. **Load**: Data is inserted into the **fact** and **dimension tables** in the star schema.

### Why Use Staging Tables?
- Staging tables **store raw data before transformation**.
- This approach ensures data integrity before inserting into final tables.
- It allows bulk loading from S3 to Redshift which is faster than inserting row-by-row.

## Project Files
- **`sql_queries.py`**: Contains SQL queries to create, drop, and insert data into tables.
- **`create_tables.py`**: Creates and resets database tables.
- **`etl.py`**: Extracts data from S3, loads it into staging tables, and inserts it into analytical tables.
- **`dwh.cfg`**: Configuration file containing AWS credentials, S3 paths, and Redshift cluster details.


## How ro run the project?
1. **Create Tables**: Run `python create_tables.py` to set up the schema.
2. **Load Staging Tables**:  RUN `etl.py` to  extracts data from S3 to staging tables in Redshift.
3. **Check data in redshift**:  RUN ```sql
SELECT COUNT(*) FROM songplays;
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM songs;
SELECT COUNT(*) FROM artists;
SELECT COUNT(*) FROM time;
```

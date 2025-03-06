# Data Warehouse with AWS Redshift

## Project Overview
This project builds an ETL pipeline to extract, transform, and load (ETL) data from AWS S3 into Amazon Redshift for Sparkify, a music streaming startup. The pipeline processes JSON log and song metadata to create an optimized star schema database for analytics.

## Dataset
- **Song Dataset**: Contains metadata about songs and artists (extracted from the Million Song Dataset).
- **Log Dataset**: Contains user activity logs for music playback.

## Database Schema (Star Schema)

### Fact Table:
- **`songplays`**: Stores records of song plays (events with `page='NextSong'`).
  - **Columns**: `songplay_id`, `start_time`, `user_id`, `level`, `song_id`, `artist_id`, `session_id`, `location`, `user_agent`

### Dimension Tables:
- **`users`**: Stores user details (`user_id`, `first_name`, `last_name`, `gender`, `level`)
- **`songs`**: Stores song metadata (`song_id`, `title`, `artist_id`, `year`, `duration`)
- **`artists`**: Stores artist metadata (`artist_id`, `name`, `location`, `latitude`, `longitude`)
- **`time`**: Stores timestamps of song plays (`start_time`, `hour`, `day`, `week`, `month`, `year`, `weekday`)

## Project Files
- **`sql_queries.py`**: Contains SQL queries to create, drop, and insert data into tables.
- **`create_tables.py`**: Creates and resets database tables.
- **`etl.py`**: Extracts data from S3, loads it into staging tables, and inserts it into analytical tables.
- **`dwh.cfg`**: Configuration file containing AWS credentials, S3 paths, and Redshift cluster details.

## ETL Pipeline
1. **Create Tables**: Run `python create_tables.py` to set up the schema.
2. **Load Staging Tables**: `etl.py` extracts data from S3 to staging tables in Redshift.
3. **Transform & Load**: Data is transformed and inserted into fact/dimension tables.
4. **Query Data**: Run SQL queries to analyze song plays.

## Example Queries
- **Most played songs:**
  ```sql
  SELECT s.title, COUNT(*) AS play_count 
  FROM songplays sp 
  JOIN songs s ON sp.song_id = s.song_id 
  GROUP BY s.title 
  ORDER BY play_count DESC 
  LIMIT 10;

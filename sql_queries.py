import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

# CREATE TABLES
staging_events_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_events (
        artist VARCHAR,
        auth VARCHAR,
        firstName VARCHAR,
        gender CHAR(1),
        itemInSession INTEGER,
        lastName VARCHAR,
        length FLOAT,
        level VARCHAR,
        location VARCHAR,
        method VARCHAR,
        page VARCHAR,
        registration BIGINT,
        sessionId INTEGER,
        song VARCHAR,
        status INTEGER,
        ts VARCHAR,
        userAgent VARCHAR,
        userId INTEGER
    );
""")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_songs (
        num_songs INTEGER,
        artist_id VARCHAR,
        artist_latitude FLOAT,
        artist_longitude FLOAT,
        artist_location VARCHAR,
        artist_name VARCHAR,
        song_id VARCHAR,
        title VARCHAR,
        duration FLOAT,
        year INTEGER
    );
""")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays (
        songplay_id INT IDENTITY(0,1) PRIMARY KEY,
        start_time TIMESTAMP NOT NULL,
        user_id INTEGER NOT NULL,
        level VARCHAR,
        song_id VARCHAR,
        artist_id VARCHAR,
        session_id INTEGER,
        location VARCHAR,
        user_agent VARCHAR
    );
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY distkey,
        first_name VARCHAR,
        last_name VARCHAR,
        gender CHAR(1),
        level VARCHAR
    );
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs (
        song_id VARCHAR PRIMARY KEY,
        title VARCHAR,
        artist_id VARCHAR distkey,
        year INTEGER sortkey,
        duration FLOAT
    );
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists (
        artist_id VARCHAR PRIMARY KEY distkey,
        name VARCHAR,
        location VARCHAR sortkey,
        latitude FLOAT,
        longitude FLOAT
    );
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time (
        start_time TIMESTAMP PRIMARY KEY sortkey distkey,
        hour INTEGER,
        day INTEGER,
        week INTEGER,
        month INTEGER,
        year INTEGER,
        weekday INTEGER
    );
""")

# STAGING TABLES

staging_events_copy = ("""
    COPY staging_events FROM {}
    IAM_ROLE {}
    FORMAT AS JSON {}
    REGION 'us-west-2';
""").format(config['S3']['LOG_DATA'], config['IAM_ROLE']['ARN'], config['S3']['LOG_JSONPATH'])

staging_songs_copy = ("""
    COPY staging_songs FROM {}
    IAM_ROLE {}
    FORMAT AS JSON 'auto'
    REGION 'us-west-2';
""").format(config['S3']['SONG_DATA'], config['IAM_ROLE']['ARN'])

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT DISTINCT TIMESTAMP 'epoch' + (e.ts / 1000) * INTERVAL '1 second',
           e.userId, e.level, s.song_id, s.artist_id, e.sessionId, e.location, e.userAgent
    FROM staging_events e
    LEFT JOIN staging_songs s ON e.song = s.title AND e.artist = s.artist_name
    WHERE e.page = 'NextSong';
""")

user_table_insert = ("""
    INSERT INTO users (user_id, first_name, last_name, gender, level)
    SELECT DISTINCT userId, firstName, lastName, gender, level
    FROM staging_events
    WHERE userId IS NOT NULL;
""")

song_table_insert = ("""
    INSERT INTO songs (song_id, title, artist_id, year, duration)
    SELECT DISTINCT song_id, title, artist_id, year, duration
    FROM staging_songs;
""")

artist_table_insert = ("""
    INSERT INTO artists (artist_id, name, location, latitude, longitude)
    SELECT DISTINCT artist_id, artist_name, artist_location, artist_latitude, artist_longitude
    FROM staging_songs;
""")

time_table_insert = ("""
    INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    SELECT DISTINCT TIMESTAMP 'epoch' + ts::BIGINT / 1000 * INTERVAL '1 second',
           EXTRACT(HOUR FROM TIMESTAMP 'epoch' + ts::BIGINT / 1000 * INTERVAL '1 second'),
           EXTRACT(DAY FROM TIMESTAMP 'epoch' + ts::BIGINT / 1000 * INTERVAL '1 second'),
           EXTRACT(WEEK FROM TIMESTAMP 'epoch' + ts::BIGINT / 1000 * INTERVAL '1 second'),
           EXTRACT(MONTH FROM TIMESTAMP 'epoch' + ts::BIGINT / 1000 * INTERVAL '1 second'),
           EXTRACT(YEAR FROM TIMESTAMP 'epoch' + ts::BIGINT / 1000 * INTERVAL '1 second'),
           EXTRACT(DOW FROM TIMESTAMP 'epoch' + ts::BIGINT / 1000 * INTERVAL '1 second')
    FROM staging_events;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]

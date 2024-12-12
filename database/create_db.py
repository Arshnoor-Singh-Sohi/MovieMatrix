# pylint: disable=broad-exception-caught
import sqlite3
import csv

def create_table(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS movies (
        tconst TEXT PRIMARY KEY,
        titleType TEXT,
        primaryTitle TEXT,
        originalTitle TEXT,
        isAdult INTEGER,
        startYear INTEGER,
        endYear INTEGER,
        runtimeMinutes INTEGER,
        genres TEXT
    )
    ''')

def insert_data(cursor, data):
    cursor.execute('''
    INSERT OR REPLACE INTO movies 
    (tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)

# Connect to the database
conn = sqlite3.connect('movies_database.db')
cursor = conn.cursor()

# Create table if it doesn't exist
create_table(cursor)

# Read and insert data from TSV file
with open('title.basics.tsv', 'r', encoding='utf-8') as tsvfile:
    tsvreader = csv.reader(tsvfile, delimiter='\t')
    next(tsvreader)  # Skip the header row
    for row in tsvreader:
        # Convert '\N' to None and handle data types
        try:
            processed_row = [
                row[0],  # tconst
                row[1],  # titleType
                row[2],  # primaryTitle
                row[3],  # originalTitle
                int(row[4]),  # isAdult
                int(row[5]) if row[5] != '\\N' else None,  # startYear
                int(row[6]) if row[6] != '\\N' else None,  # endYear
                int(row[7]) if row[7].isdigit() else None,  # runtimeMinutes
                row[8]  # genres
            ]
            insert_data(cursor, processed_row)
        except Exception as e:
            print(f"Error processing row: {row}")
            print(f"Error message: {str(e)}")

# Commit changes and close connection
conn.commit()
conn.close()

print("Data inserted successfully.")

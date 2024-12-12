import pandas as pd
import sqlite3

# Read the TSV file
df = pd.read_csv('title.basics.tsv', sep='\t', compression='gzip')

# Select relevant columns and filter for movies
movies_df = df[df['titleType'] == 'movie'][['tconst', 'primaryTitle', 'startYear', 'genres', 'runtimeMinutes']]

# Rename columns for clarity
movies_df.columns = ['id', 'title', 'release_year', 'genre', 'runtime_minutes']

# Create SQLite database
conn = sqlite3.connect('movie_database.db')

# Store data in the database
movies_df.to_sql('movies', conn, if_exists='replace', index=False)

conn.close()

print("Database created successfully.")

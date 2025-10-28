# Movie Data Pipeline for MovieLens + OMDb

import pandas as pd
import requests
from sqlalchemy import create_engine
import time
import os

# Database connection setup
engine = create_engine('sqlite:///movies.db')

# Step 1: Load local CSV files
print("Loading CSV files...")
movies_df = pd.read_csv('movies.csv')
ratings_df = pd.read_csv('ratings.csv')

movies_df['clean_title'] = movies_df['title'].str.replace(r'\(\d{4}\)', '', regex=True).str.strip()

# -------------------------------
# Step 2: Prepare new columns
# -------------------------------
for col in ['director', 'plot', 'box_office', 'year']:
    if col not in movies_df.columns:
        movies_df[col] = None

# Step 3: OMDb Config

API_KEY = 'd31ef84b'  # replace with valid key
BASE_URL = 'http://www.omdbapi.com/'

# Step 4: Fetch details safely
def get_movie_details(title, year=None):
    """Fetch movie details from OMDb safely with fallback."""
    try:
        params = {'t': title, 'apikey': API_KEY}
        if year:
            params['y'] = year

        r = requests.get(BASE_URL, params=params, timeout=10)
        data = r.json()

        # Handle rate limit or error
        if data.get('Error') == 'Request limit reached!':
            print("OMDb daily limit reached — stopping further requests.")
            return 'LIMIT_REACHED'

        if data.get('Response') != 'True':
            # Try search fallback
            search = requests.get(BASE_URL, params={'s': title, 'apikey': API_KEY}, timeout=10).json()
            if search.get('Response') == 'True':
                imdb_id = search['Search'][0]['imdbID']
                data = requests.get(BASE_URL, params={'i': imdb_id, 'apikey': API_KEY}, timeout=10).json()
            else:
                return None

        if data.get('Response') != 'True':
            return None

        # Clean up 'N/A'
        def clean(v): return None if v in ('N/A', '', None) else v

        return {
            'director': clean(data.get('Director')),
            'plot': clean(data.get('Plot')),
            'box_office': clean(data.get('BoxOffice')),
            'year': clean(data.get('Year')),
        }

    except Exception as e:
        print(f"Error fetching {title}: {e}")
        return None
    
# Step 5: Iterate & Fetch

print("Fetching data from OMDb API...")
for idx, row in movies_df.iterrows():
    title = row['clean_title']
    print(f"Fetching data for: {title}")

    details = get_movie_details(title)

    if details == 'LIMIT_REACHED':
        break

    if details:
        for key, value in details.items():
            movies_df.at[idx, key] = value
    else:
        print(f"No data found for: {title}")

    time.sleep(1)

# Step 6: Save to SQLite

print(" Saving data into SQLite database...")
movies_df.to_sql('movies', con=engine, if_exists='replace', index=False)
ratings_df.to_sql('ratings', con=engine, if_exists='replace', index=False)

# Extra: expanded genres table
genres_expanded = (
    movies_df.assign(genres=movies_df['genres'].str.split('|'))
    .explode('genres')
)
genres_expanded.to_sql('movies_expanded', con=engine, if_exists='replace', index=False)

print(" Data successfully loaded into movies.db!")
print(f"Movies: {len(movies_df)}  |  Ratings: {len(ratings_df)}")

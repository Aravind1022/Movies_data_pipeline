# Movies_data_pipeline
This project demonstrates an end-to-end data engineering pipeline that extracts, transforms, and loads (ETL) movie data from multiple sources into a relational database for analytical querying.
The pipeline integrates data from:
Local CSV files (MovieLens dataset) – containing basic movie and rating information.
External API (OMDb API) – providing enriched movie metadata such as Director, Plot, Box Office, and IMDb Rating.
Once the data is processed, it is stored in a SQLite database and analyzed through SQL queries to extract meaningful insights such as top-rated movies, most popular genres, and director statistics.

# 📁 Project Structure
Movies_Data_Pipeline_Project/
│
├── etl.py               # Main ETL script (Extract, Transform, Load)
├── schema.sql           # SQL script to create database schema
├── queries.sql          # Analytical SQL queries
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation

#⚙️ Technologies Used
Component       	Tool / Library
Language        	Python 3.x
Database        	SQLite
API             	OMDb API
Libraries	        pandas, requests, sqlalchemy
IDE	              Visual Studio Code
Extension       	SQLite Viewer (VS Code)

#🧩 Data Sources
🎞 1. Local CSV Files
From the MovieLens Small Dataset:
👉 https://grouplens.org/datasets/movielens/latest/

Files used:
movies.csv → Contains movie titles and genres
ratings.csv → Contains user ratings for movies

🌐 2. External API (OMDb API)
The OMDb API
 is used to enrich movies with extra details such as:
Director
Plot
Box Office earnings
You can register and get a free API key from OMDb API Key Registration

#⚙️ Environment Setup

1. Create and Activate a Virtual Environment
cd D:\Movies_data_pipeline_project
python -m venv venv
venv\Scripts\activate

2. Install Dependencies
Install required libraries using:
pip install -r requirements.txt
Typical requirements.txt includes:
pandas
sqlalchemy
requests

3. Database Setup
You can use SQLite for simplicity.
Run the schema setup script in your SQLite environment or directly through VS Code SQLite Viewer:
.read schema.sql
This creates the necessary tables for movies, ratings, and additional details.

#🧱 Database Design
Database Used: SQLite
SQLite is chosen for its simplicity and ease of setup for local projects.
Schema Overview
The database has two main tables:
movies — Stores all movie-related metadata (local + API-enriched).
ratings — Stores user ratings for each movie.

#🔄 ETL Pipeline Workflow
The etl.py script performs the entire ETL process:
1️⃣ Extract
Reads data from movies.csv and ratings.csv (MovieLens dataset).
For each movie, fetches additional metadata from the OMDb API using movie title or IMDb ID.
2️⃣ Transform
Cleans and preprocesses the data (handles nulls, duplicates, and data types).
Parses genre strings (splits | into separate genre entries).
Adds derived fields such as release decade.
Combines local CSV and API data into enriched datasets.
3️⃣ Load
Connects to the SQLite database using SQLAlchemy.
Loads data into the respective tables defined in schema.sql.
Ensures idempotency (re-running the script doesn’t duplicate entries).
▶️ Running the Pipeline
Once your environment is set up, run:
python etl.py
This will:
Read and clean CSV data.
Call the OMDb API for enrichment.
Load all processed data into the SQLite database (movies.db).
You can verify your database content using the SQLite Viewer extension in VS Code.

#🧩 Assumptions
1. **Dataset Structure**  
   - The MovieLens dataset (movies.csv and ratings.csv) is correctly formatted and does not contain corrupted rows.
   - Each `movieId` in `ratings.csv` corresponds to an existing record in `movies.csv`.
2. **OMDb API Responses**  
   - The OMDb API returns consistent JSON data with fields such as `Director`, `Plot`, `BoxOffice`, and `Year`.
   - Some movie titles in MovieLens may not exactly match OMDb entries due to naming or year mismatches, so a fallback search logic (`s=`) is used.
3. **Data Enrichment Logic**  
   - If OMDb does not return a movie, that record remains in the dataset with `NULL` for director, plot, and box_office.
   - The movie title is the primary matching key for OMDb lookups.
4. **Database and Environment**  
   - SQLite is used as a lightweight, file-based relational database for simplicity.
   - Running the pipeline multiple times will replace the existing data (`if_exists='replace'`) to maintain idempotency.
  
# 🚧 Challenges Faced and How I Overcame Them
1. API Title Mismatches  
Problem:  
Many movie titles in the MovieLens dataset didn’t exactly match the OMDb API’s naming conventions (e.g., “Toy Story (1995)” vs “Toy Story”).  
Solution:
Used a regular expression to remove year patterns from titles and implemented a fallback search (`s=` query) in OMDb when direct title lookup (`t=`) failed.  
This improved data match accuracy and reduced missing records.


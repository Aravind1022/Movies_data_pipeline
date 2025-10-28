-- Movies table
CREATE TABLE IF NOT EXISTS movies (
    movie_id INTEGER PRIMARY KEY,
    title TEXT,
    genres TEXT,
    director TEXT,
    plot TEXT,
    box_office TEXT,
    year INTEGER
);

-- Ratings table
CREATE TABLE IF NOT EXISTS ratings (
    user_id INTEGER,
    movie_id INTEGER,
    rating REAL,
    timestamp INTEGER,
    FOREIGN KEY(movie_id) REFERENCES movies(movie_id)
);

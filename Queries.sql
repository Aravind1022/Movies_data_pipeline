-- Analytical Queries for Movie Data Pipeline

-- 1. Which movie has the highest average rating?
SELECT 
    m.title AS Movie_Title,
    ROUND(AVG(r.rating), 2) AS Average_Rating
FROM movies m
JOIN ratings r ON m.movieId = r.movieId
GROUP BY m.movieId, m.title
ORDER BY Average_Rating DESC
LIMIT 1;


-- 2. Top 5 movie genres with the highest average rating
-- (Movies may have multiple genres separated by "|", so we use LIKE for partial matches)
SELECT 
    m.genres AS Genre,
    ROUND(AVG(r.rating), 2) AS Average_Rating
FROM movies m
JOIN ratings r ON m.movieId = r.movieId
GROUP BY m.genres
ORDER BY Average_Rating DESC
LIMIT 5;


-- 3. Who is the director with the most movies in this dataset?
SELECT 
    director,
    COUNT(*) AS Movie_Count
FROM movies
WHERE director IS NOT NULL AND director != 'N/A'
GROUP BY director
ORDER BY Movie_Count DESC
LIMIT 1;


-- 4. What is the average rating of movies released each year?
SELECT 
    year AS Release_Year,
    ROUND(AVG(r.rating), 2) AS Average_Rating
FROM movies m
JOIN ratings r ON m.movieId = r.movieId
WHERE year IS NOT NULL
GROUP BY year
ORDER BY year ASC;


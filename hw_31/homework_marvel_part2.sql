-- Задание 1
SELECT ALIVE, COUNT(*) AS count
FROM MarvelCharacters
GROUP BY ALIVE;
;

-- Задание 2
SELECT EYE AS color, AVG(APPEARANCES) AS avg_appearances
FROM MarvelCharacters
WHERE EYE IS NOT NULL
GROUP BY EYE;
;

-- Задание 3
SELECT HAIR AS color, MAX(APPEARANCES) AS max_appearances
FROM MarvelCharacters
WHERE HAIR IS NOT NULL
GROUP BY HAIR;
;

-- Задание 4
SELECT identify AS identity, MIN(APPEARANCES) AS min_appearances
FROM MarvelCharacters
WHERE identify = 'Public Identity'
GROUP BY identify;
;

-- Задание 5
SELECT SEX AS name, COUNT(*) AS count
FROM MarvelCharacters
GROUP BY SEX;
;

-- Задание 6
SELECT identify AS identity, AVG(Year) AS avg_year
FROM MarvelCharacters
WHERE identify IS NOT NULL AND Year IS NOT NULL
GROUP BY identify;
;

-- Задание 7
SELECT EYE AS color, COUNT(*) AS count
FROM MarvelCharacters
WHERE ALIVE = 'Living Characters'
GROUP BY EYE;
;

-- Задание 8
SELECT HAIR AS color, MAX(APPEARANCES) AS max_appearances, MIN(APPEARANCES) AS min_appearances
FROM MarvelCharacters
WHERE HAIR IS NOT NULL
GROUP BY HAIR;
;

-- Задание 9
SELECT identify AS identity, COUNT(*) AS count
FROM MarvelCharacters
WHERE ALIVE = 'Deceased Characters'
GROUP BY identify;
;

-- Задание 10
SELECT EYE AS color, AVG(Year) AS avg_year
FROM MarvelCharacters
WHERE EYE IS NOT NULL AND Year IS NOT NULL
GROUP BY EYE;
;

-- Задание 11
SELECT name, APPEARANCES
FROM MarvelCharacters
WHERE APPEARANCES = (SELECT MAX(APPEARANCES) FROM MarvelCharacters);
;

-- Задание 12
SELECT name, Year
FROM MarvelCharacters
WHERE Year = (
    SELECT Year 
    FROM MarvelCharacters 
    WHERE APPEARANCES = (SELECT MAX(APPEARANCES) FROM MarvelCharacters)
    LIMIT 1
);
;

-- Задание 13
SELECT name, APPEARANCES
FROM MarvelCharacters
WHERE ALIVE = 'Living Characters'
  AND APPEARANCES = (
      SELECT MIN(APPEARANCES) 
      FROM MarvelCharacters 
      WHERE ALIVE = 'Living Characters'
  );
;

-- Задание 14
SELECT name, HAIR AS color, APPEARANCES
FROM MarvelCharacters
WHERE APPEARANCES = (
    SELECT MAX(APPEARANCES) 
    FROM MarvelCharacters 
    WHERE HAIR = MarvelCharacters.HAIR
);
;

-- Задание 15
SELECT name, identify AS identity, APPEARANCES
FROM MarvelCharacters
WHERE identify = 'Public Identity'
  AND APPEARANCES = (
      SELECT MIN(APPEARANCES) 
      FROM MarvelCharacters 
      WHERE identify = 'Public Identity'
  );
;
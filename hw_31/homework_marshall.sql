-- Задание 1: Лысые злодеи 90-х годов
SELECT 
    name, 
    Year, 
    APPEARANCES 
FROM 
    MarvelCharacters 
WHERE 
    HAIR = 'No Hair' 
    AND ALIGN = 'Bad Characters' 
    AND Year BETWEEN 1990 AND 1999;

-- Задание 2: Герои с тайной идентичностью и необычными глазами
SELECT 
    name, 
    Year, 
    EYE 
FROM 
    MarvelCharacters 
WHERE 
    identify = 'Secret Identity' 
    AND EYE NOT IN ('Blue Eyes', 'Brown Eyes', 'Green Eyes') 
    AND Year IS NOT NULL;

-- Задание 3: Персонажи с изменяющимся цветом волос
SELECT 
    name, 
    HAIR 
FROM 
    MarvelCharacters 
WHERE 
    HAIR = 'Variable Hair';

-- Задание 4: Женские персонажи с редким цветом глаз
SELECT    
    name, 
    EYE 
FROM 
    MarvelCharacters 
WHERE 
    SEX = 'Female Characters' 
    AND EYE IN ('Gold Eyes', 'Amber Eyes');

-- Задание 5: Персонажи без двойной идентичности, сортированные по году появления
SELECT 
    name, 
    Year 
FROM 
    MarvelCharacters 
WHERE 
    identify != 'Dual Identity' 
    OR identify IS NULL 
    OR identify = 'No Dual Identity'
ORDER BY 
    Year DESC;

-- Задание 6: Герои и злодеи с необычными прическами
SELECT 
    name, 
    ALIGN, 
    HAIR 
FROM 
    MarvelCharacters 
WHERE 
    HAIR NOT IN ('Brown Hair', 'Black Hair', 'Blond Hair', 'Red Hair') 
    AND ALIGN IN ('Good Characters', 'Bad Characters');

-- Задание 7: Персонажи, появившиеся в 1960-е годы
SELECT 
    name, 
    Year 
FROM 
    MarvelCharacters 
WHERE 
    Year BETWEEN 1960 AND 1969;

-- Задание 8: Персонажи с уникальным сочетанием цвета глаз и волос
SELECT 
    name, 
    EYE, 
    HAIR 
FROM 
    MarvelCharacters 
WHERE 
    EYE = 'Yellow Eyes' 
    AND HAIR = 'Red Hair';

-- Задание 9: Персонажи с ограниченным количеством появлений
SELECT 
    name, 
    APPEARANCES 
FROM 
    MarvelCharacters 
WHERE 
    APPEARANCES < 10;

-- Задание 10: Персонажи с наибольшим количеством появлений (топ-5)
SELECT 
    name, 
    APPEARANCES 
FROM 
    MarvelCharacters 
ORDER BY 
    APPEARANCES DESC 
LIMIT 5;
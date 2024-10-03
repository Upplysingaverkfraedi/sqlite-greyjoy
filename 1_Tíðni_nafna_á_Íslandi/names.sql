-- Búa til töflu fyrir eiginnöfn með dálki 'Type' sem hefur sjálfgefið gildi 'First'
CREATE TABLE IF NOT EXISTS first_names (
    name TEXT,
    year INTEGER,
    count INTEGER,
    type TEXT
);

-- Búa til tímabundna töflu fyrir innlestur úr 'first_names_freq.csv'
CREATE TEMP TABLE temp_first_names (
    col1 TEXT,
    col2 INTEGER,
    col3 INTEGER
);

-- Hlaða gögn úr 'first_names_freq.csv' inn í 'temp_first_names'
.mode csv
.import 'data/first_names_freq.csv' temp_first_names

-- Flytja gögnin í töfluna 'first_names' og bæta við 'First' í dálkinn 'type'
INSERT INTO first_names (name, year, count, type)
SELECT col1, col2, col3, 'First'
FROM temp_first_names;

-- Eyða tímabundnu töflunni
DROP TABLE temp_first_names;


-- Búa til töflu fyrir millinöfn með dálki 'Type' sem hefur sjálfgefið gildi 'Middle'
CREATE TABLE IF NOT EXISTS middle_names (
    name TEXT,
    year INTEGER,
    count INTEGER,
    type TEXT
);

-- Búa til tímabundna töflu fyrir innlestur úr 'middle_names_freq.csv'
CREATE TEMP TABLE temp_middle_names (
    col1 TEXT,
    col2 INTEGER,
    col3 INTEGER
);

-- Hlaða gögn úr 'middle_names_freq.csv', sleppa fyrstu línunni (hausnum)
.mode csv
.import --skip 1 'data/middle_names_freq.csv' temp_middle_names

-- Flytja gögnin í töfluna 'middle_names' og bæta við 'Middle' í dálkinn 'type'
INSERT INTO middle_names (name, year, count, type)
SELECT col1, col2, col3, 'Middle'
FROM temp_middle_names;

-- Eyða tímabundnu töflunni
DROP TABLE temp_middle_names;


-- Sameina töflurnar 'first_names' og 'middle_names' í nýja töflu 'all_names'
CREATE TABLE IF NOT EXISTS all_names AS
SELECT * FROM first_names
UNION ALL
SELECT * FROM middle_names;

-- Eyða tímabundnu töflunum ef þær eru ekki lengur nauðsynlegar
DROP TABLE IF EXISTS first_names;
DROP TABLE IF EXISTS middle_names;

-- 1. Hvaða hópmeðlimur á algengasta eiginnafnið?
SELECT '1. Hvaða hópmeðlimur á algengasta eiginnafnið?' AS section
UNION ALL
SELECT 'Einar: ' || SUM(count) AS result
FROM all_names
WHERE name = 'Einar' AND type = 'First'
UNION ALL
SELECT 'Guðný: ' || SUM(count) AS result
FROM all_names
WHERE name = 'Guðný' AND type = 'First'
UNION ALL
SELECT 'Halldór: ' || SUM(count) AS result
FROM all_names
WHERE name = 'Halldór' AND type = 'First'
UNION ALL
SELECT 'Valur: ' || SUM(count) AS result
FROM all_names
WHERE name = 'Valur' AND type = 'First'
UNION ALL
SELECT name || ' er með algengasta nafnið' AS result
FROM (
    SELECT name, SUM(count) AS total_count
    FROM all_names
    WHERE name IN ('Einar', 'Guðný', 'Halldór', 'Valur') AND type = 'First'
    GROUP BY name
    ORDER BY total_count DESC
    LIMIT 1
);


-- 2. Hvenær voru öll nöfnin vinsælust? (Bæði eiginnöfn og millinöfn)
SELECT '2. Hvenær voru öll nöfnin vinsælust?' AS section
UNION ALL
SELECT 'Einar: ' || (SELECT year FROM all_names WHERE name = 'Einar' ORDER BY count DESC, year ASC LIMIT 1) AS result
UNION ALL
SELECT 'Guðný: ' || (SELECT year FROM all_names WHERE name = 'Guðný' ORDER BY count DESC, year ASC LIMIT 1) AS result
UNION ALL
SELECT 'Halldór: ' || (SELECT year FROM all_names WHERE name = 'Halldór' ORDER BY count DESC, year ASC LIMIT 1) AS result
UNION ALL
SELECT 'Valur: ' || (SELECT year FROM all_names WHERE name = 'Valur' ORDER BY count DESC, year ASC LIMIT 1) AS result;


-- 3. Hvenær komu þau fyrst fram? (Bæði eiginnöfn og millinöfn)
SELECT '3. Hvenær komu þau fyrst fram?' AS section
UNION ALL
SELECT 'Einar: ' || MIN(year) AS result
FROM all_names
WHERE name = 'Einar'
UNION ALL
SELECT 'Guðný: ' || MIN(year) AS result
FROM all_names
WHERE name = 'Guðný'
UNION ALL
SELECT 'Halldór: ' || MIN(year) AS result
FROM all_names
WHERE name = 'Halldór'
UNION ALL
SELECT 'Valur: ' || MIN(year) AS result
FROM all_names
WHERE name = 'Valur';
CREATE CONSTRAINT person_name_exists IF NOT EXISTS
ON (n:Person)
ASSERT EXISTS (n.name);
CREATE CONSTRAINT title_name_exists IF NOT EXISTS
ON (n:Title)
ASSERT EXISTS (n.name);
CREATE CONSTRAINT movie_year_valid IF NOT EXISTS
ON (n:Movie)
ASSERT EXISTS (n.year);
CREATE CONSTRAINT show_year_valid IF NOT EXISTS
ON (n:Show)
ASSERT EXISTS (n.year_start)

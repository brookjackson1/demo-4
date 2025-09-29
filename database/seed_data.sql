-- Sample data for Countries and Cities application
-- Run this after creating the schema to populate with sample records

-- Insert sample countries
INSERT INTO countries (country_name, country_code, continent, population) VALUES
('United States', 'USA', 'North America', 331900000),
('Canada', 'CAN', 'North America', 38000000),
('United Kingdom', 'GBR', 'Europe', 67000000),
('France', 'FRA', 'Europe', 68000000),
('Germany', 'DEU', 'Europe', 83000000),
('Japan', 'JPN', 'Asia', 125800000),
('Australia', 'AUS', 'Oceania', 25700000),
('Brazil', 'BRA', 'South America', 215000000),
('India', 'IND', 'Asia', 1380000000),
('China', 'CHN', 'Asia', 1440000000);

-- Insert sample cities
INSERT INTO cities (city_name, country_id, population, is_capital) VALUES
-- United States cities
('Washington D.C.', 1, 700000, TRUE),
('New York', 1, 8400000, FALSE),
('Los Angeles', 1, 4000000, FALSE),
('Chicago', 1, 2700000, FALSE),

-- Canada cities
('Ottawa', 2, 1000000, TRUE),
('Toronto', 2, 2930000, FALSE),
('Vancouver', 2, 2500000, FALSE),

-- United Kingdom cities
('London', 3, 9000000, TRUE),
('Manchester', 3, 2700000, FALSE),
('Birmingham', 3, 1140000, FALSE),

-- France cities
('Paris', 4, 2160000, TRUE),
('Lyon', 4, 520000, FALSE),
('Marseille', 4, 870000, FALSE),

-- Germany cities
('Berlin', 5, 3700000, TRUE),
('Munich', 5, 1500000, FALSE),
('Hamburg', 5, 1900000, FALSE),

-- Japan cities
('Tokyo', 6, 14000000, TRUE),
('Osaka', 6, 2700000, FALSE),
('Kyoto', 6, 1460000, FALSE),

-- Australia cities
('Canberra', 7, 430000, TRUE),
('Sydney', 7, 5300000, FALSE),
('Melbourne', 7, 5100000, FALSE),

-- Brazil cities
('Brasília', 8, 3100000, TRUE),
('São Paulo', 8, 12300000, FALSE),
('Rio de Janeiro', 8, 6700000, FALSE),

-- India cities
('New Delhi', 9, 32900000, TRUE),
('Mumbai', 9, 20700000, FALSE),
('Bangalore', 9, 12300000, FALSE),

-- China cities
('Beijing', 10, 21500000, TRUE),
('Shanghai', 10, 28500000, FALSE),
('Guangzhou', 10, 15300000, FALSE);
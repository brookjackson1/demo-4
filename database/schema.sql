-- Database Schema for Countries and Cities Application
-- Run this file to create the required database structure

-- Create countries table
CREATE TABLE countries (
    country_id INT AUTO_INCREMENT PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL UNIQUE,
    country_code VARCHAR(3) NOT NULL UNIQUE,
    continent VARCHAR(50),
    population BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create cities table with foreign key to countries
CREATE TABLE cities (
    city_id INT AUTO_INCREMENT PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    country_id INT NOT NULL,
    population INT,
    is_capital BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Foreign key constraint with CASCADE
    CONSTRAINT fk_cities_country
        FOREIGN KEY (country_id)
        REFERENCES countries(country_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Add indexes for common queries
CREATE INDEX idx_countries_name ON countries (country_name);
CREATE INDEX idx_countries_code ON countries (country_code);
CREATE INDEX idx_cities_name ON cities (city_name);
CREATE INDEX idx_cities_country ON cities (country_id);
CREATE INDEX idx_cities_capital ON cities (is_capital);
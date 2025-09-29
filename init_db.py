#!/usr/bin/env python3
"""
Database initialization script
Run this script to create tables and populate with seed data
"""

import os
import pymysql
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_database_connection():
    """Create a database connection using environment variables"""
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            charset='utf8mb4'
        )
        print(f"Connected to database: {os.getenv('DB_NAME')}")
        return connection
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

def execute_sql_file(connection, file_path):
    """Execute SQL commands from a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()

        # Split SQL statements by semicolon and execute them
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]

        with connection.cursor() as cursor:
            for statement in statements:
                if statement:
                    cursor.execute(statement)
                    print(f"Executed: {statement[:50]}...")

        connection.commit()
        print(f"Successfully executed {file_path}")
        return True

    except Exception as e:
        print(f"Error executing {file_path}: {e}")
        connection.rollback()
        return False

def main():
    """Main function to initialize the database"""
    print("Starting database initialization...")

    # Create database connection
    connection = create_database_connection()
    if not connection:
        print("Failed to connect to database. Check your .env file.")
        return

    try:
        # Execute schema file
        schema_path = os.path.join('database', 'schema.sql')
        if os.path.exists(schema_path):
            print("Creating database schema...")
            if not execute_sql_file(connection, schema_path):
                return
        else:
            print(f"Schema file not found: {schema_path}")
            return

        # Execute seed data file
        seed_path = os.path.join('database', 'seed_data.sql')
        if os.path.exists(seed_path):
            print("Populating with seed data...")
            if not execute_sql_file(connection, seed_path):
                return
        else:
            print(f"Seed data file not found: {seed_path}")
            return

        print("Database initialization completed successfully!")

    finally:
        connection.close()
        print("Database connection closed.")

if __name__ == "__main__":
    main()
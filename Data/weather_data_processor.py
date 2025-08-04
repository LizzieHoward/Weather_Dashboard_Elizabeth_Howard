import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime
import csv

def create_database():
    """Create SQLite database with standardized static_data table"""
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    
    # Drop existing static_data table if it exists
    cursor.execute('DROP TABLE IF EXISTS static_data')
    
    # Create the static_data table
    cursor.execute('''
        CREATE TABLE static_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            temp REAL,
            feels_like REAL,
            humidity INTEGER,
            description TEXT,
            speed REAL,
            dt TEXT
        )
    ''')
    
    conn.commit()
    return conn

def standardize_tobi_data():
    """Process weather_data_Capstone_Tobi.csv"""
    df = pd.read_csv('weather_data_Capstone_Tobi.csv')
    standardized = pd.DataFrame({
        'name': df['city'],
        'temp': df['temp_f'],
        'feels_like': np.nan,  # Not provided in original
        'humidity': df['humidity_pct'],
        'description': df['description'].str.lower(),
        'speed': df['wind_speed_mph'],
        'dt': df['datetime']
    })
    return standardized

def standardize_eric_data():
    """Process weather_data_Eric.csv"""
    df = pd.read_csv('weather_data_Eric.csv')
    standardized = pd.DataFrame({
        'name': df['city'],
        'temp': df['temperature'],
        'feels_like': df['feels_like'],
        'humidity': df['humidity'],
        'description': df['weather_description'].str.lower(),
        'speed': df['wind_speed'],
        'dt': df['timestamp']
    })
    return standardized

def standardize_shomari_data():
    """Process weather_data_Shomari.csv"""
    df = pd.read_csv('weather_data_Shomari.csv')
    standardized = pd.DataFrame({
        'name': df['City'],
        'temp': df['Temperature (F)'],
        'feels_like': np.nan,
        'humidity': np.nan,
        'description': df['Description'].str.lower(),
        'speed': np.nan,
        'dt': df['Timestamp']
    })
    return standardized

def standardize_dunasha_data():
    """Process weather_history_Dunasha.csv"""
    df = pd.read_csv('weather_history_Dunasha.csv', header=None, names=['dt', 'name', 'temp', 'description'])
    standardized = pd.DataFrame({
        'name': df['name'],
        'temp': df['temp'],
        'feels_like': np.nan,
        'humidity': np.nan,
        'description': df['description'].str.lower(),
        'speed': np.nan,
        'dt': df['dt']
    })
    return standardized

def standardize_elizabeth_data():
    """Process weather_data_Elizabeth.csv (reference format)"""
    df = pd.read_csv('weather_data_Elizabeth (1).csv')
    standardized = pd.DataFrame({
        'name': df['name'],
        'temp': df['temp'],
        'feels_like': df['feels_like'],
        'humidity': df['humidity'],
        'description': df['description'].str.lower(),
        'speed': df['speed'],
        'dt': df['dt']
    })
    return standardized

def main():
    """Main function to process all files and create database"""
    print("Creating SQLite database...")
    conn = create_database()
    
    datasets = []
    
    print("Processing Tobi's data...")
    tobi_data = standardize_tobi_data()
    datasets.append(tobi_data)
    
    print("Processing Eric's data...")
    eric_data = standardize_eric_data()
    datasets.append(eric_data)
    
    print("Processing Shomari's data...")
    shomari_data = standardize_shomari_data()
    datasets.append(shomari_data)
    
    print("Processing Dunasha's data...")
    dunasha_data = standardize_dunasha_data()
    datasets.append(dunasha_data)
    
    print("Processing Elizabeth's data...")
    elizabeth_data = standardize_elizabeth_data()
    datasets.append(elizabeth_data)
    
    print("Combining all datasets...")
    combined_data = pd.concat(datasets, ignore_index=True)
    
    print("Standardizing datetime formats...")
    combined_data['dt'] = pd.to_datetime(combined_data['dt'], errors='coerce')
    combined_data['dt'] = combined_data['dt'].dt.strftime('%Y-%m-%d %H:%M:%S')
    combined_data = combined_data.dropna(subset=['dt'])
    
    print("Inserting data into static_data table...")
    combined_data.to_sql('static_data', conn, if_exists='append', index=False)
    
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM static_data")
    total_records = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT name) FROM static_data")
    unique_cities = cursor.fetchone()[0]
    
    cursor.execute("SELECT name, COUNT(*) as count FROM static_data GROUP BY name ORDER BY count DESC LIMIT 10")
    top_cities = cursor.fetchall()
    
    print(f"\nDatabase created successfully!")
    print(f"Total records: {total_records}")
    print(f"Unique cities: {unique_cities}")
    print(f"\nTop 10 cities by record count:")
    for city, count in top_cities:
        print(f"  {city}: {count} records")
    
    print(f"\nSample data (first 5 records):")
    cursor.execute("SELECT * FROM static_data LIMIT 5")
    columns = [description[0] for description in cursor.description]
    print(f"Columns: {', '.join(columns)}")
    for row in cursor.fetchall():
        print(f"  {row}")
    
    conn.close()
    print(f"\nDatabase saved as 'weather_data.db'")

if __name__ == "__main__":

    main()
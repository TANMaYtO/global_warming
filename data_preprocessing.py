import pandas as pd
import mysql.connector

# Load the dataset
df = pd.read_csv("temperature_data.csv")

# Rename columns for easier access
df.rename(columns={
    'YEAR': 'Year',
    'ANNUAL': 'AnnualTemperature',
    'WINTER': 'WinterTemperature',
    'SUMMER': 'SummerTemperature'
}, inplace=True)

# Drop rows with missing values
df.dropna(inplace=True)

# Ensure 'Year' is an integer
df['Year'] = df['Year'].astype(int)

# Connect to MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Gobargas@123",  # Replace with your password
    database="global_warming"
)
cursor = db_connection.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS temperature_data (
    Year INT,
    AnnualTemperature FLOAT,
    WinterTemperature FLOAT,
    SummerTemperature FLOAT
)
""")

# Insert data into table
for _, row in df.iterrows():
    cursor.execute("""
    INSERT INTO temperature_data (Year, AnnualTemperature, WinterTemperature, SummerTemperature)
    VALUES (%s, %s, %s, %s)
    """, (row['Year'], row['AnnualTemperature'], row['WinterTemperature'], row['SummerTemperature']))

# Commit and close connection
db_connection.commit()
db_connection.close()
print("Data successfully loaded into the database.")

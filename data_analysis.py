import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector
import pandas as pd

# Connect to the MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Gobargas@123",  # Replace with your password
    database="global_warming"
)
cursor = db_connection.cursor(dictionary=True)

# Fetch data
cursor.execute("SELECT * FROM temperature_data")
data = cursor.fetchall()

# Convert to DataFrame
df = pd.DataFrame(data)

# Debugging: Check data structure
print("Data Preview:")
print(df.head())

print("\nColumn Names:")
print(df.columns)

# Ensure columns are numeric
df['YEAR'] = pd.to_numeric(df['YEAR'], errors='coerce')
df['AnnualTemperature'] = pd.to_numeric(df['AnnualTemperature'], errors='coerce')
df['WinterTemperature'] = pd.to_numeric(df['WinterTemperature'], errors='coerce')
df['SummerTemperature'] = pd.to_numeric(df['SummerTemperature'], errors='coerce')

# Drop rows with invalid data
df.dropna(inplace=True)

# Visualization 1: Yearly Temperature Trend
plt.figure(figsize=(10, 6))
sns.lineplot(x=df['YEAR'], y=df['AnnualTemperature'], marker='o', label='Annual Temperature')
plt.title('Yearly Temperature Trend in India')
plt.xlabel('YEAR')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.grid(True)
plt.show()

# Visualization 2: Winter vs. Summer Temperature Comparison
plt.figure(figsize=(10, 6))
sns.lineplot(x=df['YEAR'], y=df['WinterTemperature'], label='Winter Temperature')
sns.lineplot(x=df['YEAR'], y=df['SummerTemperature'], label='Summer Temperature')
plt.title('Winter vs Summer Temperature Trends')
plt.xlabel('YEAR')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.grid(True)
plt.show()

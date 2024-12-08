from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas as pd
import mysql.connector
import numpy as np

# Connect to the MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Gobargas@123",  
    database="global_warming"
)
cursor = db_connection.cursor(dictionary=True)

# Fetch data
cursor.execute("SELECT * FROM temperature_data")
data = cursor.fetchall()
df = pd.DataFrame(data)

# Prepare data for prediction
X = df['YEAR'].values.reshape(-1, 1)
y = df['AnnualTemperature'].values

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict future temperatures
future_years = np.array([2025, 2030, 2035, 2040]).reshape(-1, 1)
predictions = model.predict(future_years)

# Display predictions
print("Future Temperature Predictions:")
for year, temp in zip(future_years.flatten(), predictions):
    print(f"Year {year}: {temp:.2f}°C")

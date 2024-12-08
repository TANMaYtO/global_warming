from flask import Flask, render_template
import mysql.connector
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
from sklearn.linear_model import LinearRegression
import numpy as np
app = Flask(__name__)

def fetch_data():
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Gobargas@123", 
        database="global_warming"
    )
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM temperature_data")
    data = cursor.fetchall()
    db_connection.close()
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    return df

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/visualize')
def visualize():
    df = fetch_data()

    # Ensure numeric columns
    df['YEAR'] = pd.to_numeric(df['YEAR'], errors='coerce')
    df['AnnualTemperature'] = pd.to_numeric(df['AnnualTemperature'], errors='coerce')
    df.dropna(inplace=True)

    # Create the plot
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=df['YEAR'], y=df['AnnualTemperature'], marker='o', label='Annual Temperature')
    plt.title('Yearly Average Temperature Trend')
    plt.xlabel('Year')
    plt.ylabel('Temperature (°C)')
    plt.grid(True)

    # Save plot to memory as base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()

    return f'<img src="data:image/png;base64,{plot_url}"/>'


@app.route('/predictions')
def predictions():
    df = fetch_data()  # Fetch data from the database

    # Ensure numeric columns
    df['YEAR'] = pd.to_numeric(df['YEAR'], errors='coerce')
    df['AnnualTemperature'] = pd.to_numeric(df['AnnualTemperature'], errors='coerce')
    df.dropna(inplace=True)

    # Prepare data for regression
    X = df['YEAR'].values.reshape(-1, 1)  # Years
    y = df['AnnualTemperature'].values.reshape(-1, 1)  # Annual Temperatures

    # Train a linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Generate future predictions (e.g., for the next 10 years)
    future_years = np.arange(df['YEAR'].max() + 1, df['YEAR'].max() + 11).reshape(-1, 1)
    future_predictions = model.predict(future_years)

    # Combine historical and future data
    future_df = pd.DataFrame({
        'YEAR': future_years.flatten(),
        'ANNUAL': future_predictions.flatten()
    })

    combined_df = pd.concat([df, future_df])

    # Plot the predictions
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=combined_df['YEAR'], y=combined_df['AnnualTemperature'], label='Predicted', linestyle='--', color='orange')
    sns.lineplot(x=df['YEAR'], y=df['AnnualTemperature'], label='Historical', color='blue')
    plt.title('Temperature Predictions for the Next 10 Years')
    plt.xlabel('Year')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.grid(True)

    # Save the plot to memory as base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()

    return f'<img src="data:image/png;base64,{plot_url}"/>'


if __name__ == '__main__':
    app.run(debug=True)

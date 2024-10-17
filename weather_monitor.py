import requests
import time
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import matplotlib.pyplot as plt  

API_KEY = '558bc4f73ddfe90f8071e2f48ac614a6'  # OpenWeatherMap API key
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'
DATA_FILE = 'weather_data.csv'
THRESHOLD_TEMP = 35  # threshold in Celsius
EMAIL_ADDRESS = 'weathertesting05@gmail.com'  # My email address
EMAIL_PASSWORD = 'opye xrwv oqct tmgp'          # My email password
ALERT_RECIPIENT = 'akashku9938@gmail.com'  # Recipient email address

def fetch_weather_data(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'  # Get temperature in Celsius
    }
    response = requests.get(BASE_URL, params=params)
    return response.json() if response.status_code == 200 else None

def process_weather_data(data):
    if data:
        main = data['main']
        weather = data['weather'][0]
        city = data['name']
        processed_data = {
            'city': city,
            'temperature': main['temp'],
            'feels_like': main['feels_like'],
            'weather_condition': weather['main'],
            'timestamp': datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')
        }
        return processed_data
    return None

def save_to_csv(data):
    df = pd.DataFrame(data)
    df.to_csv(DATA_FILE, mode='a', header=not pd.io.common.file_exists(DATA_FILE), index=False)

def daily_aggregation(file_path):
    df = pd.read_csv(file_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date

    # Group by date and city
    daily_summary = df.groupby(['date', 'city']).agg(
        average_temperature=('temperature', 'mean'),
        max_temperature=('temperature', 'max'),
        min_temperature=('temperature', 'min'),
        dominant_condition=('weather_condition', lambda x: x.mode()[0])
    ).reset_index()

    return daily_summary

def plot_daily_summary(daily_summary):
    for city in daily_summary['city'].unique():
        city_data = daily_summary[daily_summary['city'] == city]
        plt.figure(figsize=(10, 5))
        plt.plot(city_data['date'], city_data['average_temperature'], label='Average Temp', marker='o')
        plt.plot(city_data['date'], city_data['max_temperature'], label='Max Temp', linestyle='--', marker='x')
        plt.plot(city_data['date'], city_data['min_temperature'], label='Min Temp', linestyle='--', marker='s')
        plt.title(f'Daily Weather Summary for {city}')
        plt.xlabel('Date')
        plt.ylabel('Temperature (°C)')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.savefig(f'{city}_daily_summary.png')  # Save the plot as a PNG file
        plt.show()  # Display the plot

def send_email_alert(alerts):
    subject = "Weather Alert"
    body = "\n".join(alerts)

    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ALERT_RECIPIENT
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # Use the app password
            server.sendmail(EMAIL_ADDRESS, ALERT_RECIPIENT, msg.as_string())
        print("Alert email sent successfully.")
    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP Authentication Error: {e}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def check_alerts(data):
    alerts = []
    for record in data:
        if record['temperature'] > THRESHOLD_TEMP:
            alerts.append(f"Alert: {record['city']} temperature is above {THRESHOLD_TEMP}°C: {record['temperature']}°C")
    if alerts:
        send_email_alert(alerts)  # Send email if alerts are triggered
    return alerts

if __name__ == '__main__':
    weather_records = []
    while True:
        for city in CITIES:
            weather_data = fetch_weather_data(city)
            processed_data = process_weather_data(weather_data)
            if processed_data:
                weather_records.append(processed_data)
        save_to_csv(weather_records)

        # Daily aggregation
        daily_summary = daily_aggregation(DATA_FILE)
        print(daily_summary)  # Print the daily summary

        # Generate visualizations
        plot_daily_summary(daily_summary)  # Generate plots for daily summaries

        # Check for alerts
        alerts = check_alerts(weather_records)
        for alert in alerts:
            print(alert)

        weather_records = []  # Reset for the next round
        time.sleep(300)  # Wait for 5 minutes before the next fetch

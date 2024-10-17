import matplotlib.pyplot as plt

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
        plt.savefig(f'{city}_daily_summary.png') 
        plt.show()  

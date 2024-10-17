# Real-Time Data Processing System for Weather Monitoring with Rollups and Aggregates

## Overview

This project is a real-time data processing system that retrieves weather data from the OpenWeatherMap API, processes the data, generates daily summaries with rollups and aggregates, and sends alerts based on user-defined thresholds. It includes features for data visualization and can be easily extended to include additional weather parameters.

## Features

- Real-time data retrieval for specified cities in India.
- Daily weather summary calculations, including:
  - Average temperature
  - Maximum temperature
  - Minimum temperature
  - Dominant weather condition
- User-configurable alert thresholds for temperature.
- Email notifications for alerts.
- Data visualization of daily summaries.

## Prerequisites

- Python 3.x
- An OpenWeatherMap API key (sign up at [OpenWeatherMap](https://openweathermap.org/))

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/akashku01/weather_monitor.git
   cd weather_monitor

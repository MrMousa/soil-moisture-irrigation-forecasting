# Soil Moisture & Irrigation Forecasting

A machine learning project I built to see how well different models can forecast soil moisture one week ahead.

The main goal was to compare a simple persistence baseline with SARIMA, XGBoost, and LSTM models, and see whether historical soil moisture and weather information could improve the forecast.

## Data

I combined:

* **USDA SCAN** soil moisture observations
* **NASA POWER** daily weather data
* Soil moisture measurements at **2 inches**
* Daily observations from **1996 to 2026**

The weather data includes temperature, precipitation, relative humidity, wind speed, and solar radiation.

## What I did

I created features from the recent history of the data, including:

* Soil moisture lags
* Weather lags
* Rolling soil moisture averages
* Rolling precipitation
* Recent changes in soil moisture
* Seasonal features

The main task was to predict soil moisture **7 calendar days ahead**, using only information that would have been available at the time of prediction.

I compared four approaches:

* **Persistence:** today's soil moisture as the 7-day forecast
* **SARIMA:** captures temporal patterns in the soil moisture series
* **XGBoost:** uses engineered soil moisture and weather features
* **LSTM:** learns patterns from sequences of past observations

I used chronological train, validation, and test splits, along with walk-forward evaluation to see how the models behaved across different time periods.

## What I found

XGBoost performed best on the validation period and outperformed the persistence baseline in **4 of 6 walk-forward periods**.

However, the results varied considerably between periods. In some years, the much simpler persistence baseline performed better than the more complex models.

This was probably the most interesting part of the project. **A more complex model can learn useful patterns, but that does not necessarily make it more robust when the behaviour of a time series changes over time.**

## Project Structure

```text
CDC_Soil_Time_Series_Forecasting/
├── configs/
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── notebooks/
│   └── 01_soil_timeseries_forecasting.ipynb
├── results/
└── src/
    ├── data_scripts/
    ├── models/
    ├── preprocessing_scripts/
    └── evaluation_scripts/
```

## Built With

Python · Pandas · NumPy · Scikit-learn · XGBoost · TensorFlow/Keras · Statsmodels

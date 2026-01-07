import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from django.db import models

def get_stock_data(symbol):
    symbol = symbol.upper() + ".NS"
    data = yf.download(symbol, period="3mo")

    if data.empty:
        return None

    return data[['Close']]

def predict_price(data):
    data['Days'] = np.arange(len(data))
    X = data[['Days']]
    y = data['Close']

    model = LinearRegression()
    model.fit(X, y)

    future_day = [[len(data)]]
    predicted_price = model.predict(future_day)

    return round(predicted_price.item(), 2)

def predict_stock(symbol):
    data = yf.download(symbol, period="3mo")

    data = data[['Close']]
    data['Next'] = data['Close'].shift(-1)
    data.dropna(inplace=True)

    X = data[['Close']]
    y = data['Next']

    model = LinearRegression()
    model.fit(X, y)

    last_close = data[['Close']].iloc[-1].values.reshape(1, -1)
    prediction = model.predict(last_close)[0]

    # chart data (last 30 days)
    chart_data = data.tail(30)

    prices = chart_data['Close'].tolist()
    dates = chart_data.index.strftime('%d-%b').tolist()

    return round(float(prediction), 2), prices, dates

'''def get_stock_data(symbol):
    symbol = symbol.upper() + ".NS" # Append NSE suffix for Indian stocks
    data = yf.download(symbol, start="2019-01-01", end="2025-12-30") #date format: YYYY-MM-DD

    if data.empty:
        return None

    return data[['Close']]

def predict_price(data):
    data['Days'] = np.arange(len(data)) # Add a column for the number of days
    X = data[['Days']]
    y = data['Close']

    model = LinearRegression()
    model.fit(X, y) # Train the model on historical data 

    future_day = [[len(data) + 1]] # Predict the next day
    predicted_price = model.predict(future_day) # Make the prediction

    return round(float(predicted_price[0]), 2)'''
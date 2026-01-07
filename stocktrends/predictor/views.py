import json
from django.shortcuts import render
from .ml_model import get_stock_data, predict_price, predict_stock

def home(request):
    return render(request, 'index.html')


def result(request):
    
    if request.method == 'POST':
        symbol = request.POST.get('symbol')

        data = get_stock_data(symbol)

        if data is None or data.empty:
            return render(request, 'index.html', {
                'error': 'Invalid stock symbol'
            })

        # Extract close prices safely
        close_prices = data['Close'].astype(float)

        # Convert index (dates) to strings
        dates = close_prices.index.strftime('%Y-%m-%d').tolist()
        prices = close_prices.values.flatten().tolist()


        # Limit to last 60 values
        dates = dates[-60:]
        prices = prices[-60:]

        current_price = round(prices[-1], 2) # Get the latest closing price
        prediction = predict_price(data)
        trend = "up" if prediction > current_price else "down"

        return render(request, 'result.html', {
            'symbol': symbol.upper(),
            'current_price': current_price,
            'prediction': prediction,
           'dates': json.dumps(dates),     # ✅ FIX
            'prices': json.dumps(prices),  # ✅ FIX
            'trend': trend,

        })

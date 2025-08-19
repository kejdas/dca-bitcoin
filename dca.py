import matplotlib.pyplot as plt
import io
import base64
import requests
import pandas as pd
from flask import Flask, request, render_template, Response, make_response, jsonify
from datetime import datetime, timedelta

file_path = 'bitcoin_prices.xlsx'
bitcoin_prices_df = pd.read_excel(file_path, engine="openpyxl")
bitcoin_prices_df['Date'] = pd.to_datetime(bitcoin_prices_df['Date'], format='%Y-%m-%d')
bitcoin_prices_dict = dict(zip(bitcoin_prices_df['Date'].dt.date, bitcoin_prices_df['Price']))

app = Flask(__name__, static_folder='templates/static')
app.config['JSON_AS_ASCII'] = False  # Allow non-ASCII characters in JSON responses, just in case


def get_bitcoin_price_today():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin", "vs_currencies": "usd"}
    headers = {"x-api-key": "[insert_your_key]"}
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        try:
            return data["bitcoin"]["usd"]
        except KeyError:
            return f"Price is not available."
    elif response.status_code == 429:
        data = response.json()
        return f"Error: {response.status_code} - {response.json().get('error', 'Free limit of API ask reach - try again in 30 seconds.')}"

def get_bitcoin_price_from_excel(date):
    return bitcoin_prices_dict.get(date.date(), None)

def calculate_dca(investment_value, purchase_interval, start_date, end_date):
    total_investment = 0
    total_bitcoin = 0
    current_date = start_date

    while current_date <= end_date:
        if current_date.date() == datetime.today().date():
            price_on_date = get_bitcoin_price_today()
        else:
            price_on_date = get_bitcoin_price_from_excel(current_date)

        # Check if price data is available and valid
        if price_on_date is not None:  # Ensure price is valid
            bitcoin_purchased = investment_value / price_on_date
            total_investment += investment_value
            total_bitcoin += bitcoin_purchased
        else:
            print(f"Skipping {current_date}: {price_on_date}")  # Error message from API

        # Increment the date based on the purchase interval
        current_date += purchase_interval
    # Get today's price and calculate the current value
    current_price = get_bitcoin_price_today()

    price_on_end_date = get_bitcoin_price_from_excel(end_date)
    value_on_end_date = total_bitcoin * price_on_end_date

    end_date_profit = value_on_end_date - total_investment

    # Ensure that current_price is valid before using it
    if current_price is not None and isinstance(current_price, (float, int)):
        current_value = current_price * total_bitcoin
        profit = current_value - total_investment
    else:
        current_value = 0
        profit = 0

    # Calculate average cost per Bitcoin
    avg_cost = total_investment / total_bitcoin if total_bitcoin > 0 else 0

     # Log the results for debugging
    print(f"DEBUG: Current BTC price: {current_price}")
    print(f"DEBUG: Total investment: {total_investment}")
    print(f"DEBUG: Total Bitcoin purchased: {total_bitcoin}")
    print(f"DEBUG: Average cost per Bitcoin: {avg_cost}")
    print(f"DEBUG: Value on end date: {value_on_end_date}")
    print(f"DEBUG: Profit on end date: {end_date_profit}")
    print(f"DEBUG: Current Value of your BTC today: {current_value}")
    print(f"DEBUG: Current profit: {profit}")

    return {
        'total_investment': total_investment,
        'total_bitcoin': total_bitcoin,
        'avg_cost': avg_cost,
        'current_value': current_value,
        'profit': profit,
        'value_on_end_date': value_on_end_date,
        'end_date_profit': end_date_profit,
        'current_price': current_price
    }


@app.route('/', methods=['GET','POST'])
def index():
    oldest_date = bitcoin_prices_df['Date'].iloc[1]
    min_date = (oldest_date - timedelta(days=1)).strftime('%Y-%m-%d')
    max_date = datetime.today().date()

    print("Request Headers:", request.headers)
    print("Request Body:", request.data)  # Log the raw body content


    if request.method == 'POST':
        try:
            # Retrieve the JSON data sent from the client
            data = request.get_json()

            if not data:
                    return jsonify({"error": "No data provided"}), 400  # Error if no data
        # Process the data
            investment_value = float(data.get('investment_value'))
            repeat_purchase = data.get('repeat_purchase')
            start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d')
            end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d')
            # Determine the purchase interval based on the user input

            if repeat_purchase == "daily":
                purchase_interval = timedelta(days=1)
            elif repeat_purchase == "weekly":
                purchase_interval = timedelta(weeks=1)
            elif repeat_purchase == "every_two_weeks":
                purchase_interval = timedelta(weeks=2)
            elif repeat_purchase == "monthly":
                purchase_interval = timedelta(weeks=4)

            # Perform the DCA calculation
            dca_result = calculate_dca(investment_value, purchase_interval, start_date, end_date)

            # Prepare the result to send back as JSON
            result = {
                'total_investment': f"{dca_result['total_investment']:,.2f}$".replace(',', ' '),
                'total_bitcoin': f"{dca_result['total_bitcoin']:.5f} BTC",
                'avg_cost': f"{dca_result['avg_cost']:,.2f}$".replace(',', ' '),
                'current_value': f"{dca_result['current_value']:,.2f}$".replace(',', ' '),
                'profit': f"{dca_result['profit']:,.2f}".replace(',', ' '),
                'value_on_end_date': f"{dca_result['value_on_end_date']:,.2f}".replace(',', ' '),
                'end_date_profit': f"{dca_result['end_date_profit']:,.2f}".replace(',', ' '),
                'current_price': f"{dca_result['current_price']:,.2f}$".replace(',', ' ')
            }

            # Return the result as JSON
            return jsonify(result)

        except Exception as e:
            # Handle any error
            return jsonify({'error': str(e)}), 400

    # For GET requests, return the normal page
    return render_template('index.html', min_date=min_date, max_date=max_date)


@app.route('/chart')
def chart():
    investment_value = float(request.args.get('investment_value', 0))
    repeat_purchase = request.args.get('repeat_purchase', 'daily')
    start_date = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(request.args.get('end_date'), '%Y-%m-%d')

    if repeat_purchase == "daily":
        purchase_interval = timedelta(days=1)
    elif repeat_purchase == "weekly":
        purchase_interval = timedelta(weeks=1)
    elif repeat_purchase == "every_two_weeks":
        purchase_interval = timedelta(weeks=2)
    elif repeat_purchase == "monthly":
        purchase_interval = timedelta(weeks=4)

    #dca_result = calculate_dca(investment_value, purchase_interval, start_date, end_date)

    dates = []
    investments = []
    total_bitcoins = []

    total_investment = 0
    total_bitcoin = 0
    current_date = start_date

    while current_date <= end_date:
        if current_date.date() == datetime.today().date():
            price_on_date = get_bitcoin_price_today()
        else:
            price_on_date = get_bitcoin_price_from_excel(current_date)

        # Check if price data is available and valid
        if price_on_date is not None:  # Ensure price is valid
            bitcoin_purchased = investment_value / price_on_date
            total_investment += investment_value
            total_bitcoin += bitcoin_purchased

            dates.append(current_date.date())
            investments.append(total_investment)
            total_bitcoins.append(total_bitcoin)

        current_date += purchase_interval

    fig, ax1 = plt.subplots(figsize=(10,6))

    ax1.plot(dates, investments, label='Total Investment', color='blue')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Total Investment ($)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    ax2 = ax1.twinx()
    ax2.plot(dates, total_bitcoins, label='Total Bitcoin', color='orange')
    ax2.set_ylabel('Total Bitcoin (BTC)', color='orange')
    ax2.tick_params(axis='y', labelcolor='orange')

    plt.title('DCA Results Over Time')
    fig.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('chart.html', plot_url=plot_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

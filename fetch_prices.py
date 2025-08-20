import requests
import pandas as pd
from datetime import datetime, timedelta
import openpyxl
import os
import time

# API Key for CoinGecko (if required)
API_KEY = '[your_api_key]'

# Fetch historical Bitcoin prices using CoinGecko API with API Key
def get_bitcoin_price_on_date(date):
    url = f'https://api.coingecko.com/api/v3/coins/bitcoin/history?date={date}&localization=false'
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    # Check if the response contains valid data
    try:
        price = data['market_data']['current_price']['usd']
        return price
    except KeyError:
        return None

# Load the existing Excel file or create a new one if not found
def load_or_create_excel(filename):
    if os.path.exists(filename):
        df_existing = pd.read_excel(filename)
        if not df_existing.empty and 'Date' in df_existing.columns:
            # Robustly parse the Date column
            df_existing['Date'] = pd.to_datetime(df_existing['Date'], errors='coerce')
            last_date = df_existing['Date'].max()
            if pd.isna(last_date):
                last_date = datetime(2024, 12, 11)
            else:
                last_date = last_date.to_pydatetime()
        else:
            df_existing = pd.DataFrame(columns=['Date', 'Price (USD)'])
            last_date = datetime(2024, 12, 11)
    else:
        df_existing = pd.DataFrame(columns=['Date', 'Price (USD)'])
        last_date = datetime(2024, 12, 11)  # Starting point
    return df_existing, last_date

# Fetch prices for the next 5 days
def fetch_next_5_days(last_date):
    dates = []
    prices = []
    delta = timedelta(days=1)
    current_date = last_date + delta
    for _ in range(5):
        date_str_api = current_date.strftime('%d-%m-%Y')  # For API
        price = get_bitcoin_price_on_date(date_str_api)
        if price is not None:
            date_str_excel = current_date.strftime('%Y-%m-%d')  # For Excel
            price_num = round(price, 1)  # Store as float, one decimal
            dates.append(date_str_excel)
            prices.append(price_num)
        current_date += delta
    return dates, prices

# Main logic
def update_bitcoin_prices():
    excel_filename = '/app/bitcoin_prices.xlsx'
    df_existing, last_date = load_or_create_excel(excel_filename)

    # Fetch next 5 days of Bitcoin prices
    dates, prices = fetch_next_5_days(last_date)

    # Check if any new data is available
    if not dates:
        print("No new data to fetch.")
        return

    # Create a DataFrame for the new data
    new_data = pd.DataFrame({'Date': dates, 'Price': prices})

    # Ensure Date column is datetime so Excel recognizes it as a date
    new_data['Date'] = pd.to_datetime(new_data['Date'], format='%Y-%m-%d')

    # Append the new data to the existing DataFrame
    df_combined = pd.concat([df_existing, new_data]).drop_duplicates(subset='Date', keep='last')

    # Ensure Date column is datetime in the combined DataFrame
    df_combined['Date'] = pd.to_datetime(df_combined['Date'], errors='coerce')

    # Before saving, format Date as string YYYY-MM-DD (no time part)
    df_combined['Date'] = df_combined['Date'].dt.strftime('%Y-%m-%d')

    # Save the updated DataFrame to Excel
    with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
        df_combined[['Date', 'Price']].to_excel(writer, index=False, sheet_name='Bitcoin Prices')

    new_rows_count = len(new_data)
    print(f"Excel file updated successfully! {new_rows_count} new rows inserted.")
    print(f"Last date in Excel: {df_existing['Date'].max()}")  # Print last date in Excel for debugging
    print(f"Excel file path: {os.path.abspath(excel_filename)}")  # Display full path

# fetch all data
# Run the script every 1 minute
#while True:
#    update_bitcoin_prices()
#    time.sleep(60)  # Wait for 60 seconds (1 minute)

if __name__ == "__main__":
    update_bitcoin_prices()

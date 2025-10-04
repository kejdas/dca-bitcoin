# DCA Bitcoin

A lightweight Flask web app to simulate Bitcoin Dollar Cost Averaging (DCA), compute investment metrics over a historical range, and visualize progress. Historical prices come from an Excel file maintained via a small fetcher script; today's price is queried from CoinGecko.

## 🌟 Features

### DCA Simulation

* **Inputs:** purchase amount, interval (daily / weekly / every two weeks / monthly), start/end dates
* **Outputs:** total invested, total BTC, average cost, current value, profit, end-date value/profit, current BTC price

### Historical Data

* Excel-based history (`bitcoin_prices.xlsx`)
* Live price fetch for "today"

### Charting

* Server-side Matplotlib chart of cumulative investment and BTC holdings

### Simple UI

* Single-page form with AJAX; results dynamically rendered </details>

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Frontend:** HTML, CSS, JavaScript
* **Data/Processing:** pandas, openpyxl, requests, Matplotlib
* **Containerization:** Docker (multi-stage), cron inside container </details>

## 📁 File Structure

```bash
dca.py                 # Flask app, DCA calculator, endpoints
fetch_prices.py        # Fills/extends bitcoin_prices.xlsx from CoinGecko
bitcoin_prices.xlsx    # Historical prices (Date, Price)
templates/
  index.html           # UI form and results container
  chart.html           # Chart image view
  static/
    js/script.js       # Form submission, results rendering
    css/style.css      # Styles and animations
Dockerfile             # Multi-stage build; starts cron and Flask
requirements.txt       # Python dependencies
README.md              # Quickstart instructions
```

## ⚙️ How It Works

### Historical Prices

* Loaded from `bitcoin_prices.xlsx` into pandas DataFrame and dict keyed by date.

### DCA Calculation

* Iterates from start to end by selected interval
* Uses historical Excel price for past dates; live CoinGecko price for "today"
* Accumulates total invested and BTC purchased; computes averages and profits

### Chart

* `/chart` recomputes cumulative totals per interval and renders base64 PNG via Matplotlib

### Endpoints

* **GET /** – Renders `index.html` with `min_date` and `max_date`
* **POST /** – Expects JSON; returns formatted JSON results
* **GET /chart** – Returns HTML page with embedded base64 PNG chart </details>

## 🔧 Configuration

### API Key Placeholders

* `dca.py` live price: header `x-api-key: [insert_your_key]` (CoinGecko usually requires none)
* `fetch_prices.py`: `API_KEY = '[your_api_key]'` (adjust if needed)

### Excel File Path

* Local dev: `bitcoin_prices.xlsx` in project root
* Docker: `/app/bitcoin_prices.xlsx` </details>

## 🏃 Running

### Local

```bash
python dca.py
```

### 🐳 Run with Docker
1. Build the Docker Image
```bash
docker build -t dca-bitcoin .
```

2. Run the Container
```bash
docker run -d -p 8080:8080 --name dca-bitcoin dca-bitcoin
```

Now open your browser:
http://localhost:5000

* Multi-stage build; cron installed
* Cron job (daily at 10:00):

```
0 10 * * * root python /app/fetch_prices.py >> /var/log/cron.log 2>&1
```

* Updates up to 5 missing future dates in `bitcoin_prices.xlsx` </details>

## 💡 Notable Implementation Details

* **DCA Intervals:** daily, weekly, every_two_weeks, monthly (\~4 weeks)
* **Edge Cases:** skips missing dates, live price failures return error string
* **Formatting:** thousands separators added to numeric output
* **UI:** AJAX POST sends JSON; results fade-in; "Clear" resets form 

## ⚠️ Limitations and Considerations

* Live price errors can show current value/profit as 0
* Monthly interval is a 4-week approximation
* CoinGecko rate-limits may apply
* Excel updates lost if container storage is ephemeral </details>

## 🎬 Quick Demo Flow

1. Open `http://localhost:8080`
2. Enter amount, choose interval, select dates
3. Click **Calculate DCA** to see results
4. Click **View Chart** for time-series visualization </details>

# ₿itcoin DCA Calculator 

A lightweight Flask web application for simulating Bitcoin Dollar Cost Averaging (DCA) strategies. Calculate investment metrics over historical periods and visualize your progress with interactive charts.

## 🌟 Features

### DCA Simulation
- **Flexible Inputs**: Purchase amount, interval (daily/weekly/bi-weekly/monthly), custom date ranges
- **Comprehensive Metrics**: 
  - Total invested and BTC accumulated
  - Average cost per Bitcoin
  - Current value and profit
  - Historical end-date value and profit
  - Real-time Bitcoin price

### Data Management
- **Historical Prices**: Excel-based storage (`bitcoin_prices.xlsx`)
- **Live Updates**: Real-time price fetching from CoinGecko API
- **Automated Updates**: Optional cron job for daily price updates

### Visualization
- **Interactive Charts**: Server-side Matplotlib visualizations
- **Dual-Axis Graphs**: Track both investment and BTC accumulation over time
- **Base64 Embedded**: Charts rendered directly in the browser

### User Interface
- **Single-Page Application**: Clean, responsive design
- **AJAX-Powered**: Dynamic results without page reloads
- **Smooth Animations**: Fade-in effects for results display
- **Form Validation**: Date constraints and input validation

## 🛠️ Tech Stack

- **Backend**: Python 3.13, Flask
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Data Processing**: pandas, openpyxl
- **Visualization**: Matplotlib
- **API Integration**: requests, CoinGecko API
- **Containerization**: Docker (multi-stage build)
- **Fonts**: Google Fonts (Poppins)

## 📁 Project Structure

```
dca-bitcoin/
├── dca.py                      # Main Flask application
├── fetch_prices.py             # Price fetcher script
├── bitcoin_prices.xlsx         # Historical price database
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Multi-stage Docker configuration
├── README.md                   # This file
└── templates/
    ├── index.html              # Main UI
    ├── chart.html              # Chart display page
    └── static/
        ├── css/
        │   └── style.css       # Styling and animations
        ├── js/
        │   └── script.js       # Client-side logic
        └── logo/
            └── bitcoin-logo.png
```

## ⚙️ How It Works

### 1. Historical Price Loading
- Reads `bitcoin_prices.xlsx` into a pandas DataFrame
- Converts to dictionary with dates as keys for O(1) lookup
- Supports dates from the Excel file's range

### 2. DCA Calculation Engine
- Iterates from start to end date by selected interval
- For each date:
  - Uses historical Excel data for past dates
  - Fetches live price from CoinGecko for today
  - Calculates BTC purchased and accumulates totals
- Computes:
  - Average cost per Bitcoin
  - Current and end-date valuations
  - Profit/loss metrics

### 3. Chart Generation
- Recomputes cumulative investment and BTC holdings per interval
- Creates dual-axis Matplotlib chart
- Converts to base64-encoded PNG for embedding
- Displays in separate chart view

### 4. API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Renders main form with min/max date constraints |
| `/` | POST | Accepts JSON, returns DCA calculation results |
| `/chart` | GET | Generates and displays investment chart |

## 🚀 Installation & Setup

### Prerequisites
- Python 3.13+
- Docker (optional)
- CoinGecko API key (optional, for higher rate limits)

### Local Development

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd dca-bitcoin
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure API keys** (optional)
Edit `dca.py` and `fetch_prices.py`:
```python
# In dca.py (line 16)
headers = {"x-api-key": "YOUR_COINGECKO_API_KEY"}

# In fetch_prices.py (line 8)
API_KEY = 'YOUR_COINGECKO_API_KEY'
```

4. **Run the application**
```bash
python dca.py
```

5. **Access the app**
Open your browser to: `http://localhost:8080`

### Docker Deployment

1. **Build the image**
```bash
docker build -t dca-bitcoin .
```

2. **Run the container**
```bash
docker run -d -p 8080:8080 --name dca-bitcoin dca-bitcoin
```

3. **Access the app**
Navigate to: `http://localhost:8080`

### Docker Features
- **Multi-stage build**: Reduces final image size
- **Automated updates**: Cron job runs daily at 10:00 UTC
- **Log management**: Updates logged to `/var/log/cron.log`

## 🔧 Configuration

### Cron Schedule
Default: Daily at 10:00 UTC
```bash
0 10 * * * root python /app/fetch_prices.py >> /var/log/cron.log 2>&1
```

Modify in `Dockerfile` (line 31) to customize schedule.

### Purchase Intervals
- **Daily**: 1-day increments
- **Weekly**: 7-day increments
- **Every two weeks**: 14-day increments
- **Monthly**: ~4 weeks (28 days)

### Price Update Behavior
`fetch_prices.py` adds the next 5 days of historical prices when executed.

## 💡 Usage Example

1. **Open the calculator**: `http://localhost:8080`
2. **Enter investment details**:
   - Purchase Amount: $100
   - Interval: Weekly
   - Start Date: 2020-01-01
   - End Date: 2024-12-01
3. **Click "Calculate DCA"**: View your results
4. **Click "View Chart"**: See visual representation
5. **Click "Clear"**: Reset the form

## 📊 Sample Output

```
DCA Strategy Results:
├─ Total investment: 26,000.00$
├─ Total Bitcoin amount: 0.45678 BTC
├─ Average cost per Bitcoin: 56,923.45$
├─ Current Value: 45,678.90$
├─ Current profit: 19,678.90$
├─ Value on end date: 44,567.80$
├─ Profit on end date: 18,567.80$
└─ Current BTC price: 100,000.00$
```

## ⚠️ Known Limitations

- **API Rate Limits**: CoinGecko free tier has rate limits; may require 30-second wait
- **Monthly Approximation**: "Monthly" uses 28-day periods
- **Missing Data Handling**: Skips dates without price data
- **Storage Persistence**: Docker containers need volume mounts for persistent Excel data
- **Live Price Dependency**: Current value displays 0 if API fails

## 🐛 Troubleshooting

### Issue: "Free limit of API reached"
**Solution**: Wait 30 seconds and try again, or add API key for higher limits

### Issue: Chart not displaying
**Solution**: Ensure matplotlib dependencies are installed: `libfreetype6-dev`, `libpng-dev`

### Issue: Excel file not updating
**Solution**: Check cron logs: `docker exec dca-bitcoin cat /var/log/cron.log`

### Issue: Missing historical data
**Solution**: Run `fetch_prices.py` manually to populate missing dates

## 🔐 Security Notes

- API keys are hardcoded (for demo purposes)
- **Production**: Use environment variables for sensitive data
- **Recommendation**: Implement `.env` file with `python-dotenv`

## 🚦 Deployment Options

### Google Cloud Platform (GCP)
Tutorial: [YouTube - Deploy Flask to GCP](https://www.youtube.com/watch?v=V0Uw8wtpDEM)

## 📝 License

This project is provided as-is for educational purposes.

## 🙏 Acknowledgments

- **CoinGecko API**: Historical and real-time Bitcoin prices
- **Flask**: Web framework
- **Matplotlib**: Chart generation
- **Google Fonts**: Poppins font family

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

**⚡ Quick Start Commands:**
```bash
# Local
python dca.py

# Docker
docker build -t dca-bitcoin . && docker run -d -p 8080:8080 dca-bitcoin
```

**Made with ❤️ for Bitcoin enthusiasts**

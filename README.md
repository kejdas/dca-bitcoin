# 💰 DCA Bitcoin – Dollar Cost Averaging Strategy

This project is a **web application** built with **Python (Flask)**, **HTML**, **CSS**, and **JavaScript**.  
It helps users calculate and visualize a **Dollar Cost Averaging (DCA) investment strategy** for Bitcoin.  

The app shows how much Bitcoin you’d accumulate over time, your average buy price, and your profit/loss — all based on historical price data.

---

## ✨ Features

- **📊 DCA Calculation**  
  - Total Bitcoin purchased  
  - Average cost per Bitcoin  
  - Current profit/loss  

- **📈 Historical Bitcoin Data**  
  - Fetches from **CoinGecko API** (or from Excel file with historical prices)  
  - Allows custom start and end dates  

- **📝 Interactive Form**  
  - Input investment amount  
  - Select purchase frequency (daily, weekly, monthly)  
  - Define start and end dates  

- **📑 Detailed Results**  
  - Total invested amount  
  - Total Bitcoin accumulated  
  - Average buy price  
  - Current Bitcoin value  
  - Current and projected profit  

- **📉 Chart Visualization**  
  - Dynamic chart of investment growth over time  

---

## 🛠️ Technologies

- **Backend:** Python (Flask)  
- **Frontend:** HTML, CSS, JavaScript  
- **Data:** CoinGecko API / Excel file with Bitcoin price history  
- **AJAX:** Dynamic updates without refreshing the page  

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/kejdas/dca-bitcoin
cd dca-bitcoin
```

### 2. Run Locally (without Docker)
Make sure you have Python 3.10+ installed.

```bash
pip install -r requirements.txt
python dca.py
```

The app will be available at:
http://localhost:5000

### 🐳 Run with Docker
1. Build the Docker Image
```bash
docker build -t dca-bitcoin .
```

2. Run the Container
```bash
docker run -d -p 5000:5000 --name dca-bitcoin dca-bitcoin
```

Now open your browser:
http://localhost:5000


# DCA Bitcoin - Dollar Cost Averaging Strategy

This project is a web application built with **Python (Flask)**, **HTML**, and **CSS** that allows users to calculate and visualize their **Dollar Cost Averaging (DCA)** strategy for Bitcoin investments. It dynamically calculates the total investment, total Bitcoin purchased, average cost per Bitcoin, and tracks the user's profit or loss based on historical data.

## Features
- **DCA Calculation**: Dynamically calculate the total Bitcoin purchased, average cost per Bitcoin, and current profit based on user input.
- **Bitcoin Price Data**: Fetch historical Bitcoin price data and calculate results for any given start and end date.
- **Interactive Form**: Users can input:
  - Investment amount
  - Purchase frequency (e.g., daily, weekly, monthly)
  - Start and end dates for the investment period
- **Result Visualization**: View detailed results of the DCA strategy, including:
  - Total investment
  - Total Bitcoin amount
  - Average cost per Bitcoin
  - Current value of the Bitcoin holdings
  - Current profit
  - Projected profit at the end date
- **Chart Visualization**: Link to view a dynamic chart of the investment over time.

## Technologies Used
- **Backend**: Python (Flask)
- **Frontend**: HTML, CSS, JavaScript
- **Bitcoin Data**: CoinGecko API or an Excel file containing historical Bitcoin prices
- **AJAX**: Used to fetch and display results dynamically without refreshing the page

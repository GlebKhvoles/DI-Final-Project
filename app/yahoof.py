import yfinance as yf

def fetch(ticker):
    stock_data = yf.Ticker(ticker)
    return stock_data.history(period="ytd", interval="1wk")


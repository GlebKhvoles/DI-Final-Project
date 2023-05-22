from app import db
from app.stocks import bp
from flask import request
from app.stocks.forms import StockForm
from flask import render_template, redirect, url_for
from app.models import Stock
from app.yahoof import fetch
import yfinance as yf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
import matplotlib.ticker as ticker


def generate_diagram(ticker_symbol, history):
    plt.figure(figsize=(10, 3))  
    plt.plot(history.index, history["Close"])
    plt.title(f"{ticker_symbol} Stock Price", fontsize=24)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Price", fontsize=12)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    formatter = ticker.FormatStrFormatter('$%1.2f')
    plt.gca().yaxis.set_major_formatter(formatter)

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    diagram_data = base64.b64encode(buffer.read()).decode("utf-8")

    plt.close()

    return diagram_data

@bp.route('/ticker/<ticker_symbol>', methods=['GET'])
def generate_ticker_page(ticker_symbol):
    # Fetch stock data using yfinance
    stock_data = yf.Ticker(ticker_symbol)
    history = stock_data.history(period="1y")
    history = history.resample("M").last()

    history = history.round({"Close": 1})

    # Format the Close column to have one digit after the decimal point
    history = history.apply(lambda x: round(x, 1))    
    diagram_data = generate_diagram(ticker_symbol, history)
    
    # Convert price history DataFrame to a dictionary
    price_history = history.reset_index().to_dict("records")

    return render_template("ticker.html", ticker_symbol=ticker_symbol, diagram_data=diagram_data, price_history=price_history)


@bp.route('/stocks', methods=['GET'])
def get_stocks():
    find_stock_form = StockForm()
    stocks = db.session.query(Stock.ticker).distinct().all()
    return render_template('stocks.html', find_stock_form=find_stock_form, stocks=stocks)


@bp.route('/stocks?delete_ticker=<delete_ticker>')
def post_stocks(delete_ticker):
    # # find_stock_form = StockForm()
    
    # if 'delete_ticker' in request.form:
    #     ticker_to_delete = request.form['delete_ticker']
    #     stock_to_delete = Stock.query.filter_by(ticker=ticker_to_delete).first()
    #     if stock_to_delete:
    #         db.session.delete(stock_to_delete)
    #         db.session.commit()
    # else:
    #     data = fetch(find_stock_form.stock.data)
    #     for date, row in data.iterrows():
    #         stock = Stock(ticker=find_stock_form.stock.data, date=date, price=row['Close'])
    #         db.session.add(stock)
    #         db.session.commit()
    print(delete_ticker)
    return 'ok'

    return redirect(url_for('stocks.get_stocks'))

@bp.route('/stocks/delete', methods=['POST'])
def delete_stock():
    if 'delete_ticker' in request.form:
        ticker_to_delete = request.form['delete_ticker']
        Stock.delete_stock(ticker_to_delete)
    
    return redirect(url_for('stocks.get_stocks'))






from flask import Flask, request, render_template
import yfinance as yf # type: ignore
import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
import seaborn as sns # type: ignore
import pickletools
import pickle
import io
import base64


def load_pickle():
	with open('input_date.pkl', 'rb') as f:
		obj = pickle.load(f)
  
	return obj

app = Flask(__name__, static_url_path='/static')

# Function to fetch stock data for a company for a specified time period
def fetch_stock_data(company_symbol, start_date, end_date):
    stock_data = yf.download(company_symbol, start=start_date, end=end_date)
    return stock_data

# Function for data cleaning, manipulation, and preprocessing
def clean_data(stock_data):
    # Remove any rows with missing values
    clean_stock_data = stock_data.dropna()
    # Perform any necessary data manipulation or preprocessing here
    return clean_stock_data

# Function for exploratory data analysis (EDA)
def perform_eda(stock_data):
    # Summary statistics
    description = stock_data.describe()
    # Correlation matrix
    correlation_matrix = stock_data.corr()
    return description, correlation_matrix

# Function for visualization
def visualize_data(stock_data):
    # Plot stock prices over time
    plt.figure(figsize=(10, 6))
    plt.plot(stock_data['Close'], label='Close Price')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Stock Price Over Time')
    plt.legend()
    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return plot_url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        company_symbol = request.form['company_symbol']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        
        # Fetch stock data
        stock_data = fetch_stock_data(company_symbol, start_date, end_date)

        # Clean, manipulate, and preprocess data
        clean_stock_data = clean_data(stock_data)

        # Perform exploratory data analysis (EDA)
        description, correlation_matrix = perform_eda(clean_stock_data)

        # Visualize data
        plot_url = visualize_data(clean_stock_data)

        return render_template('result.html', company_symbol=company_symbol, start_date=start_date, end_date=end_date,
                               description=description.to_html(), correlation_matrix=correlation_matrix.to_html(), plot_url=plot_url)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)

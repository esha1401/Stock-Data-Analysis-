import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

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
    summary_stats = stock_data.describe()
    # Correlation matrix
    correlation_matrix = stock_data.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap="YlGnBu")
    return {'summary_stats': summary_stats, 'correlation_matrix': correlation_matrix}

# Function for visualization
def visualize_data(stock_data):
    # Plot stock prices over time
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(stock_data['Close'], label='Close Price')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.set_title('Stock Price Over Time')
    ax.legend()
    return fig

# Main function
def main():
    # Get user input for company symbol and time period
    company_symbol = input("Enter the company symbol: ")
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    
    print("Stock Information for", company_symbol," : ")

    # Fetch stock data
    stock_data = fetch_stock_data(company_symbol, start_date, end_date)
    print(stock_data)

    # Clean, manipulate, and preprocess data
    clean_stock_data = clean_data(stock_data)

    # Perform exploratory data analysis (EDA)
    eda_results = perform_eda(clean_stock_data)

    # Visualize data
    fig = visualize_data(clean_stock_data)
    
    # Save functions and data to a pickle file
    with open('input_date.pkl', 'wb') as f:
        pickle.dump({
            'fetch_stock_data': fetch_stock_data,
            'clean_data': clean_data,
            'perform_eda': perform_eda,
            'visualize_data': visualize_data,
            'company_symbol': company_symbol,
            'start_date': start_date,
            'end_date': end_date,
            'eda_results': eda_results,
            'visualization_figure': fig
        }, f)

if __name__ == "__main__":
    main()
    
    with open('input_date.pkl','rb') as f:
        new_data=pickle.load(f)


# In[ ]:





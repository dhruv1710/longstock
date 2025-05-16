import requests
import yfinance as yf
import pandas as pd
# import pandas_ta as ta
import matplotlib.pyplot as plt

# Financial Statements
def format_statement(df, title, num_years):
    if df.empty:
        return f"{title}:\nNo data available.\n\n"
    
    # Select up to num_years (if available)
    cols = min(num_years, df.shape[1])
    df_subset = df.iloc[:, :cols]
    
    # Format with commas for thousands
    result = f"{title} (Last {cols} years):\n"
    result += df_subset.to_string(float_format="${:,.0f}".format)
    return result + "\n\n"

def get_ticker(company_name):
    """Get the ticker symbol for a company."""
    api = "https://query2.finance.yahoo.com/v1/finance/search"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    params = {"q": company_name, "quotes_count": 1, "country": "United States"}

    res = requests.get(url=api, params=params, headers={'User-Agent': user_agent})
    data = res.json()

    ticker_symbol = data['quotes'][0]['symbol']
    return ticker_symbol


def get_financial_data(ticker_symbol, num_years):
        """Fetch financial data from Yahoo Finance."""
        

        ticker_symbol = get_ticker(ticker_symbol)
        ticker = yf.Ticker(ticker_symbol)
        
        # Fetch data
        financials = ticker.financials
        balance_sheet = ticker.balance_sheet
        cashflow = ticker.cashflow
        
        # You can also get additional info
        info = ticker.info
        
        # Calculate some key ratios
        try:
            pe_ratio = info.get('trailingPE', 'N/A')
            ps_ratio = info.get('priceToSalesTrailing12Months', 'N/A')
            pb_ratio = info.get('priceToBook', 'N/A')
            
            # More advanced ratios might need calculation
            if not financials.empty and not balance_sheet.empty:
                # Recent year's EBITDA 
                if 'EBITDA' in financials.index:
                    ebitda = financials.loc['EBITDA'].iloc[0]
                    
                    # Calculate EV (Enterprise Value)
                    market_cap = info.get('marketCap', 0)
                    total_debt = 0
                    if 'Total Debt' in balance_sheet.index:
                        total_debt = balance_sheet.loc['Total Debt'].iloc[0]
                    cash = 0
                    if 'Cash' in balance_sheet.index:
                        cash = balance_sheet.loc['Cash'].iloc[0]
                    
                    enterprise_value = market_cap + total_debt - cash
                    
                    # EV/EBITDA
                    ev_to_ebitda = enterprise_value / ebitda if ebitda != 0 else 'N/A'
                else:
                    ev_to_ebitda = 'N/A (EBITDA not found)'
            else:
                ev_to_ebitda = 'N/A (Missing financial data)'
        except Exception as e:
            pe_ratio = ps_ratio = pb_ratio = ev_to_ebitda = f'Error calculating ratios: {str(e)}'
        
        # Format the data into a comprehensive report
        output = f"FINANCIAL DATA FOR {ticker_symbol}\n"
        output += "=" * 50 + "\n\n"
        
        # Basic Info
        output += "COMPANY OVERVIEW:\n"
        output += f"Name: {info.get('longName', ticker_symbol)}\n"
        output += f"Sector: {info.get('sector', 'N/A')}\n"
        output += f"Industry: {info.get('industry', 'N/A')}\n"
        output += f"Current Price: ${info.get('currentPrice', 'N/A')}\n"
        output += f"Market Cap: ${info.get('marketCap', 'N/A')}\n\n"
        
        # Key Ratios
        output += "KEY RATIOS:\n"
        output += f"P/E Ratio: {pe_ratio}\n"
        output += f"P/S Ratio: {ps_ratio}\n"
        output += f"P/B Ratio: {pb_ratio}\n"
        output += f"EV/EBITDA: {ev_to_ebitda}\n\n"
        output += format_statement(financials, "INCOME STATEMENT", num_years)
        output += format_statement(balance_sheet, "BALANCE SHEET", num_years)
        output += format_statement(cashflow, "CASH FLOW STATEMENT", num_years)
        
        return output

def chart_tool(company_name: str) -> str:
        """This is a tool that will return a 5 year chart of the company's stock price"""
        ticker =get_ticker(company_name)  # or any symbol like "SPY", "BTC-USD", etc.
        data = yf.download(ticker, period="5y")

        # Add technical indicators (optional)
        # data["SMA200"] = ta.sma(data["Close"], length=200)
        # data["RSI"] = ta.rsi(data["Close"], length=14)

        # Plot
        plt.figure(figsize=(14, 7))
        plt.plot(data["Close"], label="Close Price", color="blue")
        # plt.plot(data["SMA200"], label="SMA 200", color="orange", linestyle="--")
        # plt.title(f"{ticker} - 5 Year Price Chart with SMA200")
        plt.title(f"{ticker} - 5 Year Price Chart")
        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Save chart as PNG
        output_path = f"charts/{ticker}_5yr_chart.png"
        plt.savefig(output_path)

        print(f"Chart saved to {output_path}")  
        return output_path
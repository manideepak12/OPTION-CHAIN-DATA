import requests
import pandas as pd
from typing import Literal

# Define option type for type hints
OptionType = Literal['CE', 'PE']

# Alpha Vantage API setup
API_URL = "https://alpha-vantage.p.rapidapi.com/query"
API_KEY = "55a4cfd206msh9ab7a3b46c2a1fep1dba78jsn6d831555661b"

def get_symbol_search_data(instrument_name: str, side: OptionType) -> pd.DataFrame:
    """
    Fetches symbol search data from Alpha Vantage API for a given instrument name and formats it.

    Parameters:
        instrument_name (str): The search keyword for symbols, e.g., 'microsoft'
        side (str): Type of option to retrieve, 'PE' for Put and 'CE' for Call

    Returns:
        pd.DataFrame: DataFrame with columns - instrument_name, strike_price, side, and bid/ask.
    """
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "alpha-vantage.p.rapidapi.com"
    }
    params = {
        "function": "SYMBOL_SEARCH",
        "keywords": instrument_name,
        "datatype": "json"
    }

    # Make the API request
    response = requests.get(API_URL, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")

    # Parse response data
    data = response.json()
    symbols_data = data.get("bestMatches", [])

    # Process and convert to DataFrame with specified columns
    processed_data = []
    for symbol in symbols_data:
        processed_data.append({
            "instrument_name": symbol.get("2. name", ""),
            "strike_price": symbol.get("1. symbol", ""),  # Using symbol as a placeholder for strike_price
            "side": side,
            "bid/ask": symbol.get("9. matchScore", "")  # Using matchScore as a placeholder for bid/ask
        })

    # Create DataFrame with specified columns
    df = pd.DataFrame(processed_data, columns=["instrument_name", "strike_price", "side", "bid/ask"])
    if df.empty:
        print("No symbol data available for the specified keyword.")
    return df

# Example usage
if __name__ == "__main__":
    instrument_name = "microsoft"
    side = "CE"  # Example side, can be "CE" for Call or "PE" for Put

    # Fetch and print symbol search data for the specified instrument name
    df = get_symbol_search_data(instrument_name, side)
    print("Formatted Symbol Search Data:")
    print(df)

import pandas as pd
from typing import Literal

def calculate_option_metrics(df: pd.DataFrame, lot_size: int = 100, margin_percentage: float = 0.2) -> pd.DataFrame:
    """
    Calculates margin requirements and premium earned for option positions.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing option chain data with columns:
                          instrument_name, strike_price, side, bid/ask
        lot_size (int): Number of shares per lot (default: 100)
        margin_percentage (float): Required margin as percentage of strike price (default: 20%)
    
    Returns:
        pd.DataFrame: Original DataFrame with additional columns for margin_required and premium_earned
    """
    # Create a copy to avoid modifying the original DataFrame
    result_df = df.copy()
    
    # Convert strike_price and bid/ask to numeric values
    result_df['strike_price'] = pd.to_numeric(result_df['strike_price'], errors='coerce')
    result_df['bid/ask'] = pd.to_numeric(result_df['bid/ask'], errors='coerce')
    
    # Calculate margin required based on option type
    def calculate_margin(row):
        strike = row['strike_price']
        option_type = row['side']
        
        if option_type == 'PE':  # Put Option
            return strike * margin_percentage * lot_size
        elif option_type == 'CE':  # Call Option
            return strike * margin_percentage * lot_size
        else:
            return None
    
    # Calculate premium earned
    def calculate_premium(row):
        return row['bid/ask'] * lot_size
    
    # Add new columns
    result_df['margin_required'] = result_df.apply(calculate_margin, axis=1)
    result_df['premium_earned'] = result_df.apply(calculate_premium, axis=1)
    
    # Round values to 2 decimal places
    result_df['margin_required'] = result_df['margin_required'].round(2)
    result_df['premium_earned'] = result_df['premium_earned'].round(2)
    
    return result_df

# Example usage
if __name__ == "__main__":
    # Sample data
    sample_df = pd.DataFrame({
        'instrument_name': ['MSFT', 'MSFT'],
        'strike_price': ['300', '310'],
        'side': ['CE', 'PE'],
        'bid/ask': ['5.25', '4.80']
    })
    
    # Calculate metrics
    result = calculate_option_metrics(sample_df, lot_size=100, margin_percentage=0.2)
    print("Option Metrics:")
    print(result)
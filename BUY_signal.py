import pandas as pd

def analyze_ema_crossover(csv_file):
  """
  This function analyzes a CSV file containing stock data and identifies
  potential buy signals based on the 5-day EMA crossing above the 13-day
  and 21-day EMAs.

  Args:
      csv_file (str): Path to the CSV file containing stock data.

  Returns:
      pandas.DataFrame: A DataFrame containing the original data with
                        a new column 'Buy_Signal' indicating potential buy
                        opportunities.
  """

  # Read the CSV file into a pandas DataFrame
  df = pd.read_csv(csv_file)

  # Calculate the 5-day, 13-day, and 21-day EMAs using EWMA (exponential weighted moving average)
  df['ema_5'] = df['Close'].ewm(span=5, adjust=False).mean()
  df['ema_13'] = df['Close'].ewm(span=13, adjust=False).mean()
  df['ema_21'] = df['Close'].ewm(span=21, adjust=False).mean()

  # Identify buy signals based on EMA crossover conditions
  df['Buy_Signal'] = np.logical_and(df['ema_5'] > df['ema_13'], df['ema_5'] > df['ema_21'])

  return df

# Example usage
if __name__ == "__main__":
  csv_file = "stock_data.csv"  # Replace with your actual CSV file path
  df_with_signals = analyze_ema_crossover(csv_file)
  print(df_with_signals)
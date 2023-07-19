
import os

import matplotlib.pyplot as plt
import pandas as pd


def create_equity_df(course_data):
    """
    Creates a Pandas DataFrame object by reading in a CSV file. 
    Creates an index as a Series of Datetime objects for future 
    processing. Calculates the equity curve.

    Parameters:
    ----------
    course_data - A CSV file containing simulated data supplied with the 
        Performance Visualisation course.
    
    Returns:
    --------
    data - A Pandas DataFrame containing Date as an index, Holdings, Cash,
        Total, Returns and Equity columns.
    """
    data = pd.read_csv(
        course_data, sep=',', index_col=0, header=0, 
        names=["Date", "Holdings", "Cash", "Total", "Returns"]
    )
    data.index = pd.to_datetime(data.index)
    data['Equity'] = (1 + data['Returns']).cumprod()
    return data


def plot_equity(data):
    """
    Creates a plot of the equity curve.
    
    Parameters:
    ----------
    data - A Pandas DataFrame containing the equity curve data.
    """
    data['Equity'].plot(title="Equity Curve")
    plt.show()
    
    
if __name__ == "__main__":
    path = "/path/to/your/csv/directory"
    csv_data = "tearsheet-data.csv"
    course_data = os.path.join(path, csv_data)
    equity_df = create_equity_df(course_data)
    plot_equity(equity_df)
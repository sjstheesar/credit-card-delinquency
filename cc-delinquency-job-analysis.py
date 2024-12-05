import csv
import numpy as np
import pandas as pd
import os
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation  

import plotly.subplots as sp
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Function to download and load data
def load_data():
    """
    Load multiple CSV files into a list of DataFrames.
    
    Returns:
        List[pd.DataFrame]: A list of DataFrames containing the loaded data.
    """
    try:
        # Load multiple CSV files into a list of DataFrames
        dfs = [
            pd.read_csv('./ConsumerPriceIndex.csv', names=['DATE', 'CPIAUCSL']),
            pd.read_csv('./CPI_PrimRent_OwnerEquivalentRent.csv', names=['DATE', 'CUSR0000SEHA', 'CUSR0000SEHC01']),
            pd.read_csv('./DelinquencyCreditCLoans_DRCCLACBS.csv', names=['DATE', 'DRCCLACBS']),
            pd.read_csv('./FedFundsEffectiveRate_MonthlyAve.csv', names=['DATE', 'DFF']),
            pd.read_csv('./MULTJobHolders_Pri_FT_Sec_PT.csv', names=['DATE', 'LNU02026625']),
            pd.read_csv('./MULTJobHolders_Pri_Sec_BothFT.csv', names=['DATE', 'LNU02026631']),
            pd.read_csv('./MULTJobHolders_Pri_Sec_BothPT.csv', names=['DATE', 'LNU02026628']),
            pd.read_csv('./MULTJobHoldersPerc_ofEmployed_GENDER_MEN.csv', names=['DATE', 'LNU02026622']),
            pd.read_csv('./MULTJobHoldersPerc_ofEmployed_GENDER_WOMEN.csv', names=['DATE', 'LNU02026624']),
            pd.read_csv('./MULTJobHoldersPerc_ofEmployed.csv', names=['DATE', 'LNS12026620'])
        ]
        return dfs
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# Function to rename columns
def rename_columns(dfs):
    """
    Rename columns for each DataFrame in the list.
    
    Args:
        dfs (List[pd.DataFrame]): A list of DataFrames to rename columns for.
        
    Returns:
        List[pd.DataFrame]: A list of DataFrames with renamed columns.
    """
    try:
        # Rename columns for each DataFrame in the list
        dfs = [
            df.rename(columns={"CPIAUCSL": "ConsumerPriceIndex"}) for df in dfs[::2]
        ] + [
            df.rename(columns={"CUSR0000SEHA": "RentPrimaryResidence", "CUSR0000SEHC01": 'OwnerEquivalentRent'}) for df in dfs[1:3]
        ] + [
            df.rename(columns={"DRCCLACBS": "DelinquencyCreditCLoans"}) for df in dfs[3:4]
        ] + [
            df.rename(columns={"DFF": "FedFundsEffectiveRate_MonthlyAve"}) for df in dfs[4:5]
        ] + [
            df.rename(columns={"LNU02026625": "MULTJobHolders_Pri_FT_Sec_PT"}) for df in dfs[5:6]
        ] + [
            df.rename(columns={"LNU02026631": "MULTJobHolders_Pri_Sec_BothFT"}) for df in dfs[6:7]
        ] + [
            df.rename(columns={"LNU02026628": "MULTJobHolders_Pri_Sec_BothPT"}) for df in dfs[7:8]
        ] + [
            df.rename(columns={"LNU02026622": "MULTJobHolders_Perc_ofEmployed_M"}) for df in dfs[8:9]
        ] + [
            df.rename(columns={"LNU02026624": "MULTJobHoldersPerc_ofEmployed_W"}) for df in dfs[9:10]
        ] + [
            df.rename(columns={"LNS12026620": "MULTJobHoldersPerc_ofEmployed"}) for df in dfs[10:]
        ]
        return dfs
    except Exception as e:
        print(f"Error renaming columns: {e}")
        return None

# Function to merge dataframes
def merge_dataframes(dfs):
    """
    Concatenate all DataFrames and filter by date.
    
    Args:
        dfs (List[pd.DataFrame]): A list of DataFrames to concatenate.
        
    Returns:
        pd.DataFrame: A single DataFrame containing the merged data.
    """
    try:
        # Concatenate all DataFrames and filter by date
        combined_df = pd.concat(dfs, ignore_index=True)
        combined_df['DATE'] = pd.to_datetime(combined_df['DATE'])  
        combined_df = combined_df[combined_df['DATE'] >= '1994-01-01']
        return combined_df
    except Exception as e:
        print(f"Error merging dataframes: {e}")
        return None

# Function to calculate statistical information
def calculate_statistics(combined_df):
    """
    Group by date and calculate mean, median, and std for each column.
    
    Args:
        combined_df (pd.DataFrame): A DataFrame containing the merged data.
        
    Returns:
        pd.DataFrame: A DataFrame containing the calculated statistics.
    """
    try:
        # Group by date and calculate mean, median, and std for each column
        annual_statistics = combined_df.groupby('DATE').agg({
            'ConsumerPriceIndex': ['mean', 'median', 'std'],
            'RentPrimaryResidence': ['mean', 'median', 'std'],
            'OwnerEquivalentRent': ['mean', 'median', 'std'],
            'DelinquencyCreditCLoans': ['mean', 'median', 'std'],
            'FedFundsEffectiveRate_MonthlyAve': ['mean', 'median', 'std'],
            'MULTJobHolders_Pri_FT_Sec_PT': ['mean', 'median', 'std'],
            'MULTJobHolders_Pri_Sec_BothFT': ['mean', 'median', 'std'],
            'MULTJobHolders_Pri_Sec_BothPT': ['mean', 'median', 'std'],
            'MULTJobHolders_Perc_ofEmployed_M': ['mean', 'median', 'std'],
            'MULTJobHoldersPerc_ofEmployed_W': ['mean', 'median', 'std'],
            'MULTJobHoldersPerc_ofEmployed': ['mean', 'median', 'std']
        })
        # Calculate mode for each column
        annual_mode = combined_df.groupby('DATE').agg(lambda x: pd.Series.mode(x)[0] if len(pd.Series.mode(x)) > 0 else None)
        # Concatenate statistics and modes
        annual_combined_stats = pd.concat([annual_statistics, annual_mode.add_suffix('_mode')], axis=1)
        return annual_combined_stats
    except Exception as e:
        print(f"Error calculating statistics: {e}")
        return None

# Function to calculate differences over time
def calculate_differences(annual_combined_stats):
    """
    Calculate the difference over time for each mean column.
    
    Args:
        annual_combined_stats (pd.DataFrame): A DataFrame containing the calculated statistics.
        
    Returns:
        pd.DataFrame: A DataFrame containing the calculated differences.
    """
    try:
        # Calculate the difference over time for each mean column
        mean_columns = [
            ('ConsumerPriceIndex', 'mean'),
            ('RentPrimaryResidence', 'mean'),
            ('OwnerEquivalentRent', 'mean'),
            ('DelinquencyCreditCLoans', 'mean'),
            ('FedFundsEffectiveRate_MonthlyAve', 'mean'),
            ('MULTJobHolders_Pri_FT_Sec_PT', 'mean'),
            ('MULTJobHolders_Pri_Sec_BothFT', 'mean'),
            ('MULTJobHolders_Pri_Sec_BothPT', 'mean'),
            ('MULTJobHolders_Perc_ofEmployed_M', 'mean'),
            ('MULTJobHoldersPerc_ofEmployed_W', 'mean'),
            ('MULTJobHoldersPerc_ofEmployed', 'mean')
        ]
        for col in mean_columns:
            diff_column_name = f"{col[0]}_mean_diff"
            annual_combined_stats[diff_column_name] = annual_combined_stats[col].diff()
        return annual_combined_stats
    except Exception as e:
        print(f"Error calculating differences: {e}")
        return None

# Function to create recession periods
def create_recession_periods():
    """
    Define recession periods as a list of dictionaries.
    
    Returns:
        List[Dict[str, str]]: A list of dictionaries containing the recession periods.
    """
    try:
        # Define recession periods as a list of dictionaries
        recession_periods = [
            {'start': '2001-03-01', 'end': '2001-11-30'},
            {'start': '2007-12-01', 'end': '2009-06-30'},
            {'start': '2020-02-01', 'end': '2020-04-30'}
        ]
        return recession_periods
    except Exception as e:
        print(f"Error creating recession periods: {e}")
        return None

# Function to plot data
def plot_data(annual_combined_stats, recession_periods):
    """
    Plot the data using Plotly.
    
    Args:
        annual_combined_stats (pd.DataFrame): A DataFrame containing the calculated statistics.
        recession_periods (List[Dict[str, str]]): A list of dictionaries containing the recession periods.
    """
    try:
        # Convert recession periods to datetime
        start_dates = [datetime.strptime(period['start'], '%Y-%m-%d') for period in recession_periods]
        end_dates = [datetime.strptime(period['end'], '%Y-%m-%d') for period in recession_periods]

        # Create a figure with subplots
        fig = make_subplots(rows=3, cols=1, shared_xaxes=True, subplot_titles=[
            'Consumer Price Index (CPI)',
            'Rent and Owner Equivalent Rent',
            'Delinquency Credit Loans'
        ])

        # Plot Consumer Price Index (CPI)
        fig.add_trace(go.Scatter(x=annual_combined_stats.index, y=annual_combined_stats['ConsumerPriceIndex_mean'],
                                mode='lines', name='CPI Mean'), row=1, col=1)

        # Plot Rent and Owner Equivalent Rent
        fig.add_trace(go.Scatter(x=annual_combined_stats.index, y=annual_combined_stats['RentPrimaryResidence_mean'],
                                mode='lines', name='Rent Primary Residence Mean', row=2, col=1))
        fig.add_trace(go.Scatter(x=annual_combined_stats.index, y=annual_combined_stats['OwnerEquivalentRent_mean'],
                                mode='lines', name='Owner Equivalent Rent Mean', row=2, col=1))

        # Plot Delinquency Credit Loans
        fig.add_trace(go.Scatter(x=annual_combined_stats.index, y=annual_combined_stats['DelinquencyCreditCLoans_mean'],
                                mode='lines', name='Delinquency Credit Loans Mean', row=3, col=1))

        # Add recession periods to the plots
        for start_date, end_date in zip(start_dates, end_dates):
            fig.add_vrect(x0=start_date, x1=end_date, fillcolor="LightSkyBlue", opacity=0.2, layer='below')

        # Update layout
        fig.update_layout(title_text="Economic Indicators Over Time with Recession Periods",
                          xaxis_title="Date",
                          yaxis_title="Value")

        # Show the plot
        fig.show()
    except Exception as e:
        print(f"Error plotting data: {e}")

# Main function to run the script
def main():
    dfs = load_data()
    if dfs is None:
        return

    dfs = rename_columns(dfs)
    if dfs is None:
        return

    combined_df = merge_dataframes(dfs)
    if combined_df is None:
        return

    annual_combined_stats = calculate_statistics(combined_df)
    if annual_combined_stats is None:
        return

    annual_combined_stats = calculate_differences(annual_combined_stats)
    if annual_combined_stats is None:
        return

    recession_periods = create_recession_periods()
    if recession_periods is None:
        return

    plot_data(annual_combined_stats, recession_periods)

if __name__ == "__main__":
    main()

# Economic Data Analysis Script

## Overview
The script is designed to load, process, and visualize multiple economic indicators from CSV files. It includes functions to load data, rename columns, merge DataFrames, calculate statistics, find differences over time, define recession periods, and plot the data using Plotly.

## Prerequisites
- Python 3.x
- Pandas
- NumPy
- Matplotlib
- Plotly

You can install these libraries using pip:

```bash
pip install pandas numpy matplotlib plotly
```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo-url.git
   ```
2. Navigate to the project directory:
   ```bash
   cd your-project-directory
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Data Preparation
Ensure you have the following CSV files in the script's directory:
- ConsumerPriceIndex.csv
- CPI_PrimRent_OwnerEquivalentRent.csv
- DelinquencyCreditCLoans_DRCCLACBS.csv
- FedFundsEffectiveRate_MonthlyAve.csv
- MULTJobHolders_Pri_FT_Sec_PT.csv
- MULTJobHolders_Pri_Sec_BothFT.csv
- MULTJobHolders_Pri_Sec_BothPT.csv
- MULTJobHoldersPerc_ofEmployed_GENDER_MEN.csv
- MULTJobHoldersPerc_ofEmployed_GENDER_WOMEN.csv
- MULTJobHoldersPerc_ofEmployed.csv

## Usage
### Step-by-Step Guide
1. **Prepare the Data**:
   - Ensure you have the required CSV files in the script's directory.
2. **Run the Script**:
   - Execute the script using Python:
     ```bash
     python cc-delinquency-job-analysis.py
     ```

### Detailed Functions
1. **load_data()**
   - **Description**: Loads multiple CSV files into a list of Pandas DataFrames.
   - **Returns**: List[pd.DataFrame]

2. **rename_columns(dfs)**
   - **Description**: Renames columns for each DataFrame in the list to provide more meaningful identifiers.
   - **Parameters**:
     - `dfs`: List[pd.DataFrame] — A list of DataFrames to rename columns for.
   - **Returns**: List[pd.DataFrame]

3. **merge_dataframes(dfs)**
   - **Description**: Concatenates all DataFrames into a single one and filters by date.
   - **Parameters**:
     - `dfs`: List[pd.DataFrame] — A list of DataFrames to concatenate.
   - **Returns**: pd.DataFrame

4. **calculate_statistics(combined_df)**
   - **Description**: Groups the data by date and calculates mean, median, standard deviation (std), and mode for each relevant column.
   - **Parameters**:
     - `combined_df`: pd.DataFrame — A DataFrame containing the merged data.
   - **Returns**: pd.DataFrame

5. **calculate_differences(annual_combined_stats)**
   - **Description**: Calculates the difference over time for each mean column.
   - **Parameters**:
     - `annual_combined_stats`: pd.DataFrame — A DataFrame containing the calculated statistics.
   - **Returns**: pd.DataFrame

6. **create_recession_periods()**
   - **Description**: Defines recession periods as a list of dictionaries.
   - **Returns**: List[Dict[str, str]]

7. **plot_data(annual_combined_stats, recession_periods)**
   - **Description**: Plots the data using Plotly, including recession periods marked on the plots.
   - **Parameters**:
     - `annual_combined_stats`: pd.DataFrame — A DataFrame containing the calculated statistics.
     - `recession_periods`: List[Dict[str, str]] — A list of dictionaries containing the recession periods.

## Output
The script will generate a Plotly interactive plot displaying the trends of various economic indicators over time, marked with recession periods.

## Contributing
Contributions are welcome! Please fork the repository and submit pull requests or open issues for improvements and bug fixes.

## License
This script is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

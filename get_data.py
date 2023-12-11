## import packages
import pandas as pd
import numpy as np



## global variables
names_of_days = {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'}


### get data ----

#### get data flight
def flights_by_terminal(data, terminal):
    daily_flight = data[data['TERMINAL'] == f'{terminal}'].groupby('DATE').size().reset_index()

    # Rename columns
    df_flight = daily_flight.rename(columns={'DATE': 'Date', 0: 'Number of Flights'})

    return df_flight

#### get data pax
def pax_by_terminal(data, terminal):
    daily_pax = data[data['TERMINAL'] == f'{terminal}'].groupby('DATE')['TOTAL_PAX'].sum().reset_index()

    # Rename columns
    df_pax = daily_pax.rename(columns={'DATE': 'Date', 'TOTAL_PAX': 'Number of Passengers'})

    return df_pax

#### get data delay
def delay_by_terminal(data, terminal):
    daily_delay = data[data['TERMINAL'] == '1A'].groupby('DATE')['DELAY'].sum()

    # Convert the series to a dataframe
    df_delay = daily_delay.reset_index()
    df_delay.columns = ['Date', 'Delay']
    df_delay['Delay'] = df_delay['Delay'].astype(int)

    return df_delay

#### get avg data per day
def avg_per_day(df, column_name):
    # Ensure the 'Date' column is in datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    # Get the name of the day from the 'Date' column
    df['Day'] = df['Date'].dt.day_name()

    # Group by day and calculate the mean, then reorder according to names_of_days
    avg_data_per_day = df.groupby('Day')[f'{column_name}'].mean().reindex(names_of_days)

    # Convert the series to a dataframe and round up the values
    df_avg_data_per_day = avg_data_per_day.apply(np.ceil).astype(int).reset_index()
    df_avg_data_per_day.columns = ["Day", f"Average {column_name}"]

    return df_avg_data_per_day

#### get top categories based on number of flight
def top_categories_by_flights(data, terminal, default_column_name, new_column_name):
    top_categories = data[data['TERMINAL'] == f'{terminal}'].groupby(f'{default_column_name}').size().reset_index()

    # Rename columns
    df_top_categories = top_categories.rename(columns={f'{default_column_name}': f'{new_column_name}', 0: 'Number of Flights'})

    return df_top_categories
## import packages
import pandas as pd
import numpy as np

import plotly.graph_objects as go
import plotly.express as px



## global variables
names_of_days = {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'}



## functions

### get data ----

#### get data flight
def get_flights_by_terminal(data, terminal):
    daily_flight = data[data['TERMINAL'] == f'{terminal}'].groupby('DATE').size().reset_index()

    # Rename columns
    df_flight = daily_flight.rename(columns={'DATE': 'Date', 0: 'Number of Flights'})

    return df_flight

#### get data pax
def get_pax_by_terminal(data, terminal):
    daily_pax = data[data['TERMINAL'] == f'{terminal}'].groupby('DATE')['TOTAL_PAX'].sum().reset_index()

    # Rename columns
    df_pax = daily_pax.rename(columns={'DATE': 'Date', 'TOTAL_PAX': 'Number of Passengers'})

    return df_pax

#### get data delay
def get_delay_by_terminal(data, terminal):
    daily_delay = data[data['TERMINAL'] == '1A'].groupby('DATE')['DELAY'].sum()

    # Convert the series to a dataframe
    df_delay = daily_delay.reset_index()
    df_delay.columns = ['Date', 'Delay']
    df_delay['Delay'] = df_delay['Delay'].astype(int)

    return df_delay

#### get avg data per day
def get_avg_data_per_day(df, column_name):
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
def get_top_categories_by_flights(data, terminal, default_column_name, new_column_name):
    top_categories = data[data['TERMINAL'] == f'{terminal}'].groupby(f'{default_column_name}').size().reset_index()

    # Rename columns
    df_top_categories = top_categories.rename(columns={f'{default_column_name}': f'{new_column_name}', 0: 'Number of Flights'})

    return df_top_categories




### get info ----
def get_highest_and_lowest(data, column_name):
    min_data = data.loc[data[f"{column_name}"].idxmin()]
    max_data = data.loc[data[f"{column_name}"].idxmax()]

    print(f"Lowest {column_name}:\n", min_data)
    print("\n")
    print(f"Highest {column_name}:\n", max_data)



### generate chart ----
def generate_single_timeseries_chart(x, y, title, x_title, y_title, color, text1, text2, terminal, time):
    # Create an area chart for the revenue figures
    fig = go.Figure()

    # Define common style elements for xaxis and yaxis
    axis_style = {
        'showgrid': True,
        'showline': True,
        'showticklabels': True,
        'tickfont': {'family': 'Arial', 'size': 12, 'color': 'gray'},
    }

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode='lines+markers',
            fill='tozeroy',
            line=dict(color=f'{color}', width=2.5),
            marker=dict(color=f'{color}', size=7),
            name='',
            hovertemplate=f"%{{x| %d %b %Y}}<br>{text1}: %{{y}} {text2}",
        )
    )
    
    # Format the layout
    fig.update_layout(
        title=dict(
            text=f"{title}<br>at {terminal} - Soekarno-Hatta International Airport<br>in {time}",
            x=0.5
        ),
        xaxis_title=f'{x_title}',
        yaxis_title=f'{y_title}',
        xaxis={**axis_style, 'linecolor': 'gray', 'linewidth': 2, 'ticks': 'outside'},
        yaxis={**axis_style, 'gridcolor': 'lightgray', 'zeroline': False, 'showline': False},
        template="plotly_white",
        paper_bgcolor='white',
        plot_bgcolor='white'
    )

    return fig.show()


def generate_barchart_avg_data_per_day(df, column_name, terminal, time):
    # Sort the dataframe
    df_sorted = df.sort_values(by=f"{column_name}")

    # Create the horizontal bar chart using Plotly.graph_objects
    fig = go.Figure(data=[go.Bar(
        x=df_sorted[f"{column_name}"], 
        y=df_sorted['Day'], 
        orientation='h',
        marker=dict(
            color=df_sorted[f"{column_name}"],  # Use the values to determine the colors
            colorscale=px.colors.sequential.Plasma_r
        ), 
        text=df_sorted[f"{column_name}"],  
        textposition='outside'  
    )])

    # Update the layout
    fig.update_layout(
        height=400, 
        width=900,
        title=dict(
            text=f"{column_name} per Day<br>at {terminal} - Soekarno-Hatta International Airport<br>{time}", 
            font=dict(size=18)),
        title_x=0.5,
        title_y=0.90,
        xaxis_title=f"{column_name}", 
        yaxis_title='Day',
        yaxis=dict(
            tickfont=dict(size=20)  # Adjust font size for y-axis labels
        ),
        margin=dict(r=10, l=20, b=0, t=110, pad=5),
    )

    fig.show()
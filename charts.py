## import packages
import plotly.graph_objects as go
import plotly.express as px


### generate chart ----
def single_timeseries_chart(x, y, title, x_title, y_title, color, text1, text2, terminal, time):
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


def barchart_avg_data_per_day(df, column_name, terminal, time, text1):
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
        textposition='outside' ,
        name='',
        hovertemplate=f"%{{y}}: %{{x}} {text1}",
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

def horizontal_barchart_top_categories(df, column_name, terminal, time, title):
    # Sort the dataframe
    df_sorted = df.sort_values(by="Number of Flights")

    # Create the horizontal bar chart using Plotly.graph_objects
    fig = go.Figure(data=[go.Bar(
        x=df_sorted['Number of Flights'][-10:], 
        y=df_sorted[f'{column_name}'][-10:], 
        orientation='h',
        marker=dict(
            color=df_sorted['Number of Flights'][-10:],  # Use the values to determine the colors
            colorscale=px.colors.sequential.Plasma_r
        ), 
        text=df_sorted['Number of Flights'][-10:],  
        textposition='outside',
        name='',
        hovertemplate="%{y}: %{x} Flights",
    )])

    # Update the layout
    fig.update_layout(
        height=400, 
        width=900,
        title=dict(
            text=f"{title} (based on Number of Flights)<br>at {terminal} - Soekarno-Hatta International Airport<br>{time}", 
            font=dict(size=18)),
        title_x=0.5,
        title_y=0.90,
        xaxis_title='Number of Flights', 
        yaxis_title=f'{column_name}',
        yaxis=dict(
            tickfont=dict(size=15)  # Adjust font size for y-axis labels
        ),
        margin=dict(r=10, l=20, b=0, t=110, pad=5),
    )

    fig.show()
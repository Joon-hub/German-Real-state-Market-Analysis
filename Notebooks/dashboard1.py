import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import json

# Load data
train = pd.read_csv('path_to_your_data.csv')  # Replace with your data file
with open('../GeoJSON/germany-states2.geojson') as f:
    geojson_data = json.load(f)

# Preprocess data
train['stateName'] = train['stateName'].str.replace('_', '-')
avg_rent_by_state = train.groupby('stateName')['totalRent'].mean().reset_index()
avg_rent_by_flat_type = train.groupby('typeOfFlat')['totalRent'].mean().reset_index()
rent_trends = train.groupby(['stateName', 'date'])['totalRent'].mean().reset_index()

# Initialize Dash app
app = dash.Dash(__name__)
app.title = 'Rent Dashboard'

# Layout
app.layout = html.Div([
    html.H1("Germany Rent Analysis Dashboard", style={'textAlign': 'center'}),
    
    # Dropdown for state selection
    dcc.Dropdown(
        id='state-dropdown',
        options=[{'label': 'All States', 'value': 'all'}] +
                [{'label': state, 'value': state} for state in avg_rent_by_state['stateName']],
        value='all',
        placeholder="Select a state",
        style={'width': '50%', 'margin': 'auto'}
    ),
    
    # Graphs
    html.Div([
        dcc.Graph(id='choropleth-map'),
        dcc.Graph(id='bar-chart'),
        dcc.Graph(id='line-chart'),
        dcc.Graph(id='flat-type-bar-chart'),
    ])
])

# Callbacks
@app.callback(
    [Output('choropleth-map', 'figure'),
     Output('bar-chart', 'figure'),
     Output('line-chart', 'figure'),
     Output('flat-type-bar-chart', 'figure')],
    [Input('state-dropdown', 'value')]
)
def update_charts(selected_state):
    # Choropleth Map
    temp_df = avg_rent_by_state.copy()
    if selected_state != 'all':
        temp_df['highlight'] = temp_df['stateName'] == selected_state
    fig1 = px.choropleth(
        temp_df,
        geojson=geojson_data,
        locations='stateName',
        featureidkey='properties.name',
        color='totalRent',
        color_continuous_scale='Viridis_r',
    )
    fig1.update_geos(fitbounds="locations", visible=False)
    fig1.update_layout(title='Average Total Rent per State in Germany',
                       margin={"r": 0, "t": 50, "l": 0, "b": 0})
    
    # Bar Chart
    fig2 = px.bar(avg_rent_by_state, x='stateName', y='totalRent', text='totalRent')
    if selected_state != 'all':
        fig2.update_traces(marker_color=[
            'orange' if state == selected_state else 'blue'
            for state in avg_rent_by_state['stateName']
        ])
    fig2.update_layout(title='Average Total Rent by State', xaxis_title='State Name', yaxis_title='Average Rent (€)')
    
    # Line Chart
    filtered_trends = rent_trends.copy()
    if selected_state != 'all':
        filtered_trends = rent_trends[rent_trends['stateName'] == selected_state]
    fig3 = px.line(filtered_trends, x='date', y='totalRent', color='stateName')
    fig3.update_layout(title='Average Total Rent Trends', xaxis_title='Date', yaxis_title='Average Rent (€)')
    
    # Bar Chart for Flat Types
    fig4 = px.bar(avg_rent_by_flat_type, x='typeOfFlat', y='totalRent', text='totalRent', color='typeOfFlat')
    fig4.update_layout(title='Average Rent by Flat Type', xaxis_title='Flat Type', yaxis_title='Average Rent (€)')
    
    return fig1, fig2, fig3, fig4

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

import json
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import html, dcc, Input, Output
import plotly.io as pio
import pandas as pd

# import data
train = pd.read_csv('Data/eda_data.csv')
train = train.sample(n=1000, random_state=42).reset_index(drop=True)

# Load GeoJSON file for German states
with open('GeoJSON/germany-states2.geojson') as f:
    geojson_data = json.load(f)

# Set default Plotly theme
pio.templates.default = "plotly_white"

# State-level data preparation
avg_rent_by_state_bar = train.groupby('stateName')['totalRent'].mean().reset_index()
avg_rent_by_state_bar = avg_rent_by_state_bar.sort_values('totalRent', ascending=False)

avg_rent_by_state_line = (
    train.groupby(['stateName', 'date'])['totalRent']
    .mean()
    .reset_index()
    .sort_values(['date'], ascending=False)
)

# City-level data preparation
avg_rent_by_city_bar = train.groupby('cityName')[['totalRent', 'baseRent', 'serviceCharge']].mean().reset_index()
avg_rent_by_city_bar = avg_rent_by_city_bar.sort_values('totalRent', ascending=False)

avg_rent_by_city_line = (
    train.groupby(['cityName', 'date'])['totalRent']
    .mean()
    .reset_index()
    .sort_values(['date'], ascending=False)
)

# Create Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Germany Rent Analysis Dashboard", style={'textAlign': 'center'}),
    
    dcc.Tabs([
        # State Tab
        dcc.Tab(label='State Analysis', children=[
            html.Div([
                dcc.Dropdown(
                    id='state-dropdown',
                    options=[{'label': 'All States', 'value': 'all'}] +
                            [{'label': state, 'value': state} for state in train['stateName'].unique()],
                    value='all',
                    placeholder="Select a state",
                    style={'width': '50%', 'margin': '20px auto'}
                ),
                
                # Add metric cards for state analysis
                html.Div(id='state-metrics', className='metric-container'),
                
                html.Div([
                    html.Div([
                        dcc.Graph(id='state-rent-distribution'),
                    ], style={'width': '50%'}),
                    
                    html.Div([
                        dcc.Graph(id='state-bar-chart'),
                    ], style={'width': '50%'}),
                ], style={'display': 'flex'}),

                html.Div([
                    html.Div([
                        dcc.Graph(id='state-line-chart'),
                    ], style={'width': '50%'}),

                    html.Div([
                        dcc.Graph(id='state-heatmap'),
                    ], style={'width': '50%'}),
                ], style={'display': 'flex', 'marginTop': '20px'}),
            ]),
        ]),
        
        # City Tab
        dcc.Tab(label='City Analysis', children=[
            html.Div([
                dcc.Dropdown(
                    id='city-dropdown',
                    options=[{'label': 'All Cities', 'value': 'all'}] +
                            [{'label': city, 'value': city} for city in train['cityName'].unique()],
                    value='all',
                    placeholder="Select a city",
                    style={'width': '50%', 'margin': '20px auto'}
                ),
                
                # Add metric cards for city analysis
                html.Div(id='city-metrics', className='metric-container'),
                
                html.Div([
                    html.Div([
                        dcc.Graph(id='city-price-components'),
                    ], style={'width': '50%'}),
                    
                    html.Div([
                        dcc.Graph(id='city-features-impact'),
                    ], style={'width': '50%'}),
                ], style={'display': 'flex'}),

                html.Div([
                    html.Div([
                        dcc.Graph(id='city-year-analysis'),
                    ], style={'width': '50%'}),

                    html.Div([
                        dcc.Graph(id='city-property-types'),
                    ], style={'width': '50%'}),
                ], style={'display': 'flex', 'marginTop': '20px'}),
            ]),
        ]),
    ]),
])

@app.callback(
    [Output('state-rent-distribution', 'figure'),
     Output('state-bar-chart', 'figure'),
     Output('state-line-chart', 'figure'),
     Output('state-heatmap', 'figure'),
     Output('state-metrics', 'children')],
    [Input('state-dropdown', 'value')]
)
def update_state_charts(selected_state):
    df = train.copy()
    if selected_state != 'all':
        df = df[df['stateName'] == selected_state]
    
    # Rent Distribution
    dist_fig = px.box(
        df,
        x='stateName',
        y='totalRent',
        title='Rent Distribution by State'
    )
    
    # Bar Chart - Average Rents with highlighting
    bar_fig = px.bar(
        avg_rent_by_state_bar,
        x='stateName',
        y='totalRent',
        title='Average Total Rent by State'
    )
    
    # Update bar colors and opacity based on selection
    if selected_state != 'all':
        colors = ['rgba(31, 119, 180, 0.3)' if state != selected_state else 'rgb(31, 119, 180)' 
                 for state in avg_rent_by_state_bar['stateName']]
        bar_fig.update_traces(marker_color=colors)
    
    bar_fig.update_traces(
        texttemplate='€%{y:.2f}',
        textposition='outside'
    )
    
    # Line Chart - Trends
    line_fig = px.line(
        df.groupby(['date', 'stateName'])['totalRent'].mean().reset_index(),
        x='date',
        y='totalRent',
        color='stateName',
        title='Rent Trends Over Time'
    )
    
    # Heatmap - Correlations
    numeric_cols = ['totalRent', 'baseRent', 'serviceCharge', 'livingSpace', 'noRooms']
    corr_matrix = df[numeric_cols].corr()
    heatmap_fig = px.imshow(
        corr_matrix,
        title='Correlation Heatmap',
        labels=dict(color="Correlation")
    )
    
    # Metrics
    metrics = html.Div([
        html.Div([
            html.H4(f"Average Total Rent: €{df['totalRent'].mean():.2f}"),
            html.H4(f"Average Living Space: {df['livingSpace'].mean():.1f} m²"),
            html.H4(f"Average Rooms: {df['noRooms'].mean():.1f}"),
        ], style={'textAlign': 'center'})
    ])
    
    return dist_fig, bar_fig, line_fig, heatmap_fig, metrics

@app.callback(
    [Output('city-price-components', 'figure'),
     Output('city-features-impact', 'figure'),
     Output('city-year-analysis', 'figure'),
     Output('city-property-types', 'figure'),
     Output('city-metrics', 'children')],
    [Input('city-dropdown', 'value')]
)
def update_city_charts(selected_city):
    df = train.copy()
    if selected_city != 'all':
        df = df[df['cityName'] == selected_city]
    
    # Price Components
    components_fig = px.bar(
        avg_rent_by_city_bar.head(15),
        x='cityName',
        y=['baseRent', 'serviceCharge'],
        title='Rent Components by City (Top 15)',
        barmode='stack'
    )
    components_fig.update_layout(xaxis_tickangle=-45)
    
    # Features Impact
    features = ['balcony', 'hasKitchen', 'cellar', 'garden', 'lift']
    impact_data = []
    for feature in features:
        avg_with = df[df[feature] == 1]['totalRent'].mean()
        avg_without = df[df[feature] == 0]['totalRent'].mean()
        impact_data.append({
            'feature': feature,
            'with_feature': avg_with,
            'without_feature': avg_without
        })
    
    impact_df = pd.DataFrame(impact_data)
    features_fig = px.bar(
        impact_df,
        x='feature',
        y=['with_feature', 'without_feature'],
        title='Impact of Features on Rent',
        barmode='group',
        labels={'value': 'Average Rent (€)', 'variable': 'Feature Presence'}
    )
    
    # Year Analysis
    year_fig = px.box(
        df,
        x='yearConstructed_category',
        y='totalRent',
        title='Rent Distribution by Construction Year'
    )
    
    # Property Types
    type_fig = px.bar(
        df.groupby('typeOfFlat')['totalRent'].mean().reset_index(),
        x='typeOfFlat',
        y='totalRent',
        title='Average Rent by Property Type'
    )
    type_fig.update_traces(texttemplate='€%{y:.2f}', textposition='outside')
    
    # Metrics
    metrics = html.Div([
        html.Div([
            html.H4(f"Average Total Rent: €{df['totalRent'].mean():.2f}"),
            html.H4(f"Average Service Charge: €{df['serviceCharge'].mean():.2f}"),
            html.H4(f"Average Living Space: {df['livingSpace'].mean():.1f} m²"),
        ], style={'textAlign': 'center'})
    ])

    return components_fig, features_fig, year_fig, type_fig, metrics

if __name__ == '__main__':
    app.run_server(debug=True)
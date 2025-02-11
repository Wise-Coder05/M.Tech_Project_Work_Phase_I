import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import random  # For simulating incoming pings

historical_file_path = 'extracted_csv.csv'  # Ensure this path is correct
historical_data = pd.read_csv(historical_file_path)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

simulation_running = True

def create_fig(data):
    return px.scatter(data, x='Time', y='Length', color='Source',
                       title='Ping Flood Detection',
                       labels={'Source': 'Source IP', 'Time': 'Time (seconds)', 'Length': 'Message Size (bytes)'})

app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    html.H1(children='Ping Flood Detection Dashboard'),

    dcc.Link('Home', href='/'),
    dcc.Link('Malicious Nodes', href='/malicious-nodes'),
    
    dcc.Graph(id='ping-flood-graph', figure=create_fig(historical_data)),
    
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # in milliseconds (1 second)
        n_intervals=0,
        disabled=not simulation_running  # Disable when not running
    ),

    html.Div(id='live-update-text'),

    dbc.Button("Stop Simulation", id="stop-button", n_clicks=0),
    
    dbc.Table(id='comparison-table', bordered=True)
])

# Combined callback to update the graph and handle navigation
@app.callback(
    Output('ping-flood-graph', 'figure'),
    Output('live-update-text', 'children'),
    Output('comparison-table', 'children'),
    Output('interval-component', 'disabled'),  # Control interval based on simulation state
    Input('interval-component', 'n_intervals'),
    Input('stop-button', 'n_clicks'),
    Input('url', 'pathname')
)
def update_graph(n, stop_clicks, pathname):
    global simulation_running

    if stop_clicks > 0:
        simulation_running = False

    if not simulation_running:
        return create_fig(historical_data), "Simulation stopped.", "", True

    # Simulate incoming ping data (you would replace this with actual data collection)
    new_time = random.uniform(0, 100)  # Simulated time in seconds
    new_length = random.randint(64, 1500)  # Simulated message size in bytes
    new_source_ip = f"192.168.1.{random.randint(1, 254)}"  # Simulated source IP

    # Determine if the ping is normal or malicious based on size and frequency
    is_malicious = new_length > 1000  # Simple logic for flood detection based on size

    # Append new data to historical data for visualization
    new_data = pd.DataFrame({
        'Time': [new_time],
        'Length': [new_length],
        'Source': [new_source_ip],
        'Type': ['Malicious' if is_malicious else 'Normal']
    })

    updated_data = pd.concat([historical_data, new_data], ignore_index=True)

    # Create the comparison table with color coding
    comparison_table_header = [
        html.Tr([html.Th("Type"), html.Th("Source IP"), html.Th("Message Size (bytes)"), html.Th("Time (seconds)")]),
        html.Tbody([
            html.Tr(
                [html.Td(row['Type'], style={'backgroundColor': 'red' if row['Type'] == 'Malicious' else 'green'}),
                 html.Td(row['Source']),
                 html.Td(row['Length']),
                 html.Td(row['Time'])])
            for _, row in updated_data.iterrows()]
        )
    ]

    # Handle navigation to malicious nodes page
    if pathname == '/malicious-nodes':
        malicious_data = updated_data[updated_data['Type'] == 'Malicious']
        return create_fig(malicious_data), "Displaying Malicious Nodes", comparison_table_header, False

    return create_fig(updated_data), f'Latest Ping: Source={new_source_ip}, Size={new_length} bytes', comparison_table_header, False

# Run the app on a specific port (e.g., 8080)
if __name__ == '__main__':
    app.run_server(debug=True, port=5000)  # Change the port number here if needed
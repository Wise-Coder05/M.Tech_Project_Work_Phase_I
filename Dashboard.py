import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

# Load the dataset
file_path = 'genuine_with_label.csv'  # Ensure this path is correct
data = pd.read_csv(file_path)

# Create a Dash application
app = Dash(__name__)

# Create a scatter plot for visualization
fig = px.scatter(data, x='Duration', y='Received echo requests', color='label',
                 title='Ping Flood Detection',
                 labels={'label': 'Ping Flood (0: No, 1: Yes)', 'Duration': 'Duration (seconds)', 'Received echo requests': 'Received Echo Requests'})

# Define the layout of the dashboard
app.layout = html.Div(children=[
    html.H1(children='Ping Flood Detection Dashboard'),
    
    dcc.Graph(
        id='ping-flood-graph',
        figure=fig
    ),
    
    html.Div(children='''
        This dashboard visualizes the relationship between Duration and Received Echo Requests.
        Points colored in different colors represent whether a ping flood attack is detected.
    ''')
])

# Run the app on a specific port (e.g., 8080)
if __name__ == '__main__':
    app.run_server(debug=True, port=5000)
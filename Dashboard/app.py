import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import pandas as pd

# Sample data (replace with your own data)
# Replace 'your_data.csv' with your CSV file path
# df = pd.read_csv('output_dataset_with_keywords.csv')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("BERTopic Dashboard"),
    dcc.Graph(id='heatmap-plot', src='assets/topic_heatmap.html'),
    dcc.Graph(id='barchart-plot', src='assets/topic_barchart.html'),
    dcc.Graph(id='scatter-plot', src='assets/topic_scatter_plot.html'),
    dcc.Graph(id='hierarchy-plot', src='assets/topic_Topic_Hierarchy.html'),
    # html.Div(id='table-container', children=[
    #     dash_table.DataTable(
    #         id='topic-table',
    #         columns=[
    #             {'name': 'Topic ID', 'id': 'Topic ID'},
    #             {'name': 'Topic Name', 'id': 'Topic Name'}
    #         ],
    #         data=df
    #     )
    # ])
])

# Define callback function(s) here


if __name__ == '__main__':
    app.run_server(debug=True)

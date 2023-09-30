
import dash
import dash_table
import dash_html_components as html
import pandas as pd

app = dash.Dash(__name__)


plot1_url = "assets/topic_heatmap.html"
plot2_url = "assets/topic_scatter_plot.html"
plot3_url = "assets/topic_barchart.html"
plot4_url = "assets/topic_Topic_Hierarchy.html"


plot1_url_outlier = "assets/topic_heatmap_outlier.html"
plot2_url_outlier = "assets/topic_scatter_plot_outlier.html"
plot3_url_outlier = "assets/topic_barchart_outlier.html"
plot4_url_outlier = "assets/topic_Topic_Hierarchy_outlier.html"

unique_topics = pd.read_csv('topics.csv')

# Define the layout of your dashboard
app.layout = html.Div([
    html.H1("Analysis of irrelevant papers"),

    # Flex container
    html.Div([
        html.Div([dash_table.DataTable(
            id='topic-table',
            columns=[
                {'name': 'Topic', 'id': 'Topic'},
                {'name': 'Name', 'id': 'Name'},
                {'name': 'Count', 'id': 'Count'},
            ],
            data=unique_topics.to_dict('records'),
            # style_table={'width': '800px', 'height': '400px', 'overflowY': 'auto'},
        ),
        ], style={'width': '45%', 'display': 'inline-block', 'padding': '10px'}),  # Adjust the width as needed)

        # First Row
        html.Div([
            # 70% of viewport height
            html.Iframe(src=plot1_url, width='100%', height='1080')
        ], style={'width': '100%', 'display': 'inline-block'}),  # Adjust the width as needed),  # 6 columns width for first column


        html.Div([
            # 70% of viewport height
            html.Iframe(src=plot3_url, width='100%', height='1080')
        ], style={'width': '100%', 'display': 'inline-block'}),

    ], style={'display': 'flex'}),



    # First Row
    html.Div([
        # First Column
        html.Div([
            # 70% of viewport height
            html.Iframe(src=plot2_url, width='100%', height='700vh')
        ], style={'width': '100%', 'display': 'inline-block'}),  # 6 columns width for first column

        # Second Column
        # html.Div([
        #     # 70% of viewport height
        #     html.Iframe(src=plot3_url, width='100%', height='600vh')
        # ], style={'width': '100%', 'display': 'inline-block'}),  # 6 columns width for second column

        html.Div([
            # 70% of viewport height
            html.Iframe(src=plot4_url, width='100%', height='700vh')
        ], style={'width': '100%', 'display': 'inline-block'}),

    ], style={'display': 'flex', 'padding': '10px'}),  # Row containing two columns
    # -------------------------------------------------------------------------------------------------#
    html.H1("Analysis of irrelevant papers outliers"),
    # First Row
    html.Div([
        # First Column
        html.Div([
            # 70% of viewport height
            html.Iframe(src=plot1_url_outlier, width='100%', height='700vh')
        ], style={'width': '100%', 'display': 'inline-block'}),  # 6 columns width for first column

        # Second Column
        # html.Div([
        #     # 70% of viewport height
        #     html.Iframe(src=plot3_url, width='100%', height='600vh')
        # ], style={'width': '100%', 'display': 'inline-block'}),  # 6 columns width for second column

        html.Div([
            # 70% of viewport height
            html.Iframe(src=plot2_url_outlier, width='100%', height='700vh')
        ], style={'width': '100%', 'display': 'inline-block'}),

        html.Div([
            # 70% of viewport height
            html.Iframe(src=plot3_url_outlier, width='100%', height='700vh')
        ], style={'width': '100%', 'display': 'inline-block'}),

        html.Div([
            # 70% of viewport height
            html.Iframe(src=plot4_url_outlier, width='100%', height='700vh')
        ], style={'width': '100%', 'display': 'inline-block'}),

    ], style={'display': 'flex', 'padding': '10px'}),  # Row containing two columns

])

# app.layout = html.Div([

#     html.H1("BERTopic Dashboard"),

#     # html.Iframe(
#     #     src="assets/topic_heatmap.html",
#     #     style={"height": "1067px", "width": "40%"},
#     # ),
#     # html.Iframe(
#     #     src="assets/topic_scatter_plot.html",
#     #     style={"height": "600px", "width": "40%"},
#     # ),
#     # html.Iframe(
#     #     src="assets/topic_Topic_Hierarchy.html",
#     #     style={"height": "600px", "width": "40%"},
#     # ),
#     # html.Iframe(
#     #     src="assets/topic_barchart.html",
#     #     style={"height": "1267px", "width": "50%"},
#     # )

#     html.Div([
#         html.Iframe(
#             src="assets/topic_heatmap.html",  # Replace with the URL you want to embed
#             # Adjust width and height as needed
#             style={"width": "35%", "height": "1000px", "display": "left"},
#             # title="Embedded Website"
#         ),
#     ], style={"margin-bottom": "20px"}),

#     html.Div([
#         html.Iframe(
#             src="assets/topic_scatter_plot.html",  # Another example with a different URL
#             # Adjust width and height as needed
#             style={"width": "35%", "height": "600px", "display": "right"},
#             # title="Google"
#         ),
#     ], style={"margin-bottom": "20px"}),


#     # children=[

#     #     html.H1("BERTopic Dashboard"),
#     #     html.Iframe(
#     #         src="assets/topic_heatmap.html",
#     #         style={"height": "1067px", "width": "40%"},
#     #     ),
#     #     html.Iframe(
#     #         src="assets/topic_scatter_plot.html",
#     #         style={"height": "600px", "width": "40%"},
#     #     ),
#     #     html.Iframe(
#     #         src="assets/topic_Topic_Hierarchy.html",
#     #         style={"height": "600px", "width": "40%"},
#     #     ),
#     #     html.Iframe(
#     #         src="assets/topic_barchart.html",
#     #         style={"height": "1267px", "width": "50%"},
#     #     )
#     # ],
# ])

if __name__ == "__main__":
    app.run_server(debug=True)

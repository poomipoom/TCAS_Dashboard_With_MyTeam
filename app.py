from dash.dependencies import Input, Output, State
from dash import dcc, html
import plotly.express as px
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from flask_caching import Cache
import redis
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load data
df = pd.read_json('data/data3.json')

faculties = df['field'].unique()
tcas_rounds = ["Portfolio", "Quota", "Admission", "Direct Admission"]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.server.config['CACHE_TYPE'] = 'redis'
app.server.config['CACHE_REDIS'] = redis.Redis(host='localhost', port=6379, db=0)
cache = Cache(app.server)  # Initializing Cache instance

# Custom CSS
app.clientside_callback(
    """
    function(hoverData) {
        return hoverData ? hoverData.points[0].location : 'Hover over a point on the map for details';
    }
    """,
    Output('hover-info', 'children'),
    Input('map-graph', 'hoverData')
)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    dbc.CardHeader(html.H4("เลือกสาขาวิชาและหลักสูตร")),
                    dcc.Dropdown(id='faculty-dropdown', options=[{'label': faculty, 'value': faculty} for faculty in faculties], placeholder="เลือกสาขาวิชา", style={'color': 'black'}),
                    dcc.Dropdown(id='program-dropdown', options=[], placeholder="เลือกหลักสูตร", style={'color': 'black', "width": "100%"}),
                    html.Div(id='university-intake')
                ])
            )
        ], width=6),
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    dbc.CardHeader(html.H4("เลือกมหาวิทยาลัย")),
                    dcc.Dropdown(id='university-dropdown', options=[], placeholder="เลือกมหาวิทยาลัย", style={'color': 'black'}),
                    html.Div(id='tcas-intake')
                ])
            )
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    dbc.CardHeader(html.H4("ค่าเทอมของหลักสูตร")),
                    html.Div(id='tuition-fee')
                ])
            )
        ], width=6),
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    dbc.CardHeader(html.H4("MAP")),
                    dcc.Graph(id='map-graph')
                ])
            )
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col(html.Div(id='hover-info', style={'fontSize': '18px', 'marginTop': '10px'}), width=12)
    ])
], fluid=True)

@cache.memoize(timeout=60)  # Cache data for 60 seconds
@app.callback(
    Output('program-dropdown', 'options'),
    Input('faculty-dropdown', 'value')
)
def update_program_options(selected_faculty):
    try:
        if selected_faculty:
            filtered_programs = df[df['field'] == selected_faculty]['program'].unique()
            program_options = [{'label': program, 'value': program} for program in filtered_programs]
        else:
            program_options = []
    except Exception as e:
        logger.error(f"Error in update_program_options: {e}")
        program_options = []
    return program_options

@cache.memoize(timeout=60)  # Cache data for 60 seconds
@app.callback(
    Output('map-graph', 'figure'),
    Output('university-intake', 'children'),
    Output('university-dropdown', 'options'),
    Output('tuition-fee', 'children'),
    Input('program-dropdown', 'value'),
    Input('university-dropdown', 'value')
)
def update_university_info(selected_program, selected_university):
    try:
        # Base map with all universities
        map_fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", hover_name="university", hover_data=["program", "intake_per_course", "tuition_fee_amount"], color="university", size_max=15)
        map_fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=5, mapbox_center={"lat": 13.736717, "lon": 100.523186}, margin={"r":0,"t":0,"l":0,"b":0})

        # Filtered data for university intake
        university_intake_text = html.P("กรุณาเลือกหลักสูตร", style={"textAlign": "center"})
        university_options = []
        tuition_fee_text = "กรุณาเลือกมหาวิทยาลัย"

        if selected_program:
            filtered_df = df[df['program'] == selected_program]
            university_intake_text = html.Div([
                html.P("จำนวนการรับเข้า", style={"textAlign": "center"}),
                html.Table([
                    html.Tr([html.Th("มหาวิทยาลัย"), html.Th("รับเข้า")])
                ] + [
                    html.Tr([html.Td(row['university']), html.Td(row['intake_per_course'])]) for _, row in filtered_df.iterrows()
                ], style={"width": "100%", "border": "1px solid #ddd", "padding": "5px", "fontSize": "16px"})
            ])
            university_options = [{'label': uni, 'value': uni} for uni in filtered_df['university'].unique()]

        if selected_university and selected_program:
            filtered_university_df = filtered_df[filtered_df['university'] == selected_university]
            if not filtered_university_df.empty:
                university_info = filtered_university_df.iloc[0]
                lat, lon = university_info['latitude'], university_info['longitude']
                map_fig = px.scatter_mapbox(df[df['university'] == selected_university], lat="latitude", lon="longitude", hover_name="university", hover_data=["program"], color="university", size_max=15)
                map_fig.update_layout(mapbox_style="carto-positron", mapbox_center={'lat': lat, 'lon': lon}, mapbox_zoom=15)
                tuition_fee_text = f"{university_info['tuition_fee']}"
            else:
                map_fig.update_layout(mapbox_center={"lat": 13.736717, "lon": 100.523186}, mapbox_zoom=5)
                tuition_fee_text = "ข้อมูลไม่พบ"
        return map_fig, university_intake_text, university_options, tuition_fee_text

    except Exception as e:
        logger.error(f"Error in update_university_info: {e}")
        map_fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", hover_name="university", hover_data=["program"], color="university")
        map_fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=5, mapbox_center={"lat": 13.736717, "lon": 100.523186})
        university_intake_text = html.P("เกิดข้อผิดพลาดในการโหลดข้อมูล", style={"textAlign": "center"})
        university_options = []
        tuition_fee_text = "ข้อมูลไม่พบ"
        return map_fig, university_intake_text, university_options, tuition_fee_text

@cache.memoize(timeout=60)  # Cache data for 60 seconds
@app.callback(
    Output('tcas-intake', 'children'),
    Input('university-dropdown', 'value'),
    State('program-dropdown', 'value')
)
def update_tcas_info(selected_university, selected_program):
    try:
        if selected_university and selected_program:
            filtered_df = df[(df['university'] == selected_university) & (df['program'] == selected_program)]
            tcas_intake_text = html.Div([
                html.P("TCAS", style={"textAlign": "center"}),
                html.Table([
                    html.Tr([html.Th("รอบ TCAS"), html.Th("รับเข้า")])
                ] + [
                    html.Tr([html.Td(round), html.Td(filtered_df[round].values[0])]) for round in tcas_rounds
                ], style={"width": "100%", "border": "1px solid #ddd", "padding": "5px", "fontSize": "16px"})
            ])
        else:
            tcas_intake_text = html.P("กรุณาเลือกหลักสูตรและมหาวิทยาลัย", style={"textAlign": "center"})
    except Exception as e:
        logger.error(f"Error in update_tcas_info: {e}")
        tcas_intake_text = html.P("เกิดข้อผิดพลาดในการโหลดข้อมูล", style={"textAlign": "center"})
    return tcas_intake_text

if __name__ == '__main__':
    app.run_server(debug=True)

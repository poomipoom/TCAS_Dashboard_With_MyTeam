import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

# อ่านข้อมูลจากไฟล์ JSON
df = pd.read_json('data/data3.json')

# สร้างรายการสาขาวิชาและรอบ TCAS
faculties = df['field'].unique()
tcas_rounds = ["Portfolio", "Quota", "Admission", "Direct Admission"]

# สร้าง Dash app พร้อมกับใช้ธีม Darkly
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Define custom CSS styles
custom_styles = {
    'backgroundColor': '#333',  # Gray background color
    'padding': '20px',
    'borderRadius': '10px'
}

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H1("Engineering Courses Dashboard"),
                    dcc.Graph(id='map-graph')
                ]),
                style=custom_styles  # Apply the custom styles here
            )
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H2("เลือกสาขาวิชา"),
                    dcc.Dropdown(id='faculty-dropdown', options=[{'label': faculty, 'value': faculty} for faculty in faculties], placeholder="เลือกสาขาวิชา", style={'color': 'black'})
                ])
            )
        ], width=6),
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H2("เลือกหลักสูตร"),
                    dcc.Dropdown(id='program-dropdown', options=[], placeholder="เลือกหลักสูตร", style={'color': 'black'}),
                    html.Div(id='university-intake')
                ])
            )
        ], width=6)
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H2("เลือกมหาวิทยาลัย"),
                    dcc.Dropdown(id='university-dropdown', options=[], placeholder="เลือกมหาวิทยาลัย", style={'color': 'black'}),
                    html.Div(id='tcas-intake')
                ])
            )
        ], width=6),
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H2("ค่าเทอมของหลักสูตร"),
                    html.Div(id='tuition-fee')
                ])
            )
        ], width=6)
    ])
], fluid=True)

@app.callback(
    Output('program-dropdown', 'options'),
    Input('faculty-dropdown', 'value')
)
def update_program_options(selected_faculty):
    if selected_faculty:
        filtered_programs = df[df['field'] == selected_faculty]['program'].unique()
        program_options = [{'label': program, 'value': program} for program in filtered_programs]
    else:
        program_options = []
    return program_options

@app.callback(
    Output('map-graph', 'figure'),
    Output('university-intake', 'children'),
    Output('university-dropdown', 'options'),
    Output('tuition-fee', 'children'),
    Input('program-dropdown', 'value'),
    Input('university-dropdown', 'value')
)
def update_university_info(selected_program, selected_university):
    ctx = dash.callback_context
    map_fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", hover_name="university", hover_data=["program", "intake_per_course", "tuition_fee_amount"], color="university")
    map_fig.update_layout(mapbox_style="open-street-map", mapbox_zoom=5, mapbox_center={"lat": 13.736717, "lon": 100.523186})

    university_intake_text = "กรุณาเลือกสาขาวิชา"
    university_options = []
    tuition_fee_text = ""

    if selected_program:
        filtered_df = df[df['program'] == selected_program]
        university_intake_text = html.Ul([html.Li(f"{row['university']}: รับ {row['intake_per_course']} คน") for _, row in filtered_df.iterrows()])
        university_options = [{'label': uni, 'value': uni} for uni in filtered_df['university'].unique()]
        tuition_fee_text = f"{selected_program}: ค่าเทอม {filtered_df['tuition_fee_amount'].values[0]} บาท"

    if selected_university:
        university_info = df[df['university'] == selected_university].iloc[0]
        lat, lon = university_info['latitude'], university_info['longitude']
        map_fig = px.scatter_mapbox(df[df['university'] == selected_university], lat="latitude", lon="longitude", hover_name="university", hover_data=["program", "intake_per_course", "tuition_fee_amount"], color="university")
        map_fig.update_layout(mapbox_style="open-street-map", mapbox_center={'lat': lat, 'lon': lon}, mapbox_zoom=15)

    return map_fig, university_intake_text, university_options, tuition_fee_text

@app.callback(
    Output('tcas-intake', 'children'),
    Input('university-dropdown', 'value'),
    State('program-dropdown', 'value')
)
def update_tcas_info(selected_university, selected_program):
    if selected_university and selected_program:
        filtered_df = df[(df['university'] == selected_university) & (df['program'] == selected_program)]
        tcas_intake_text = html.Ul([html.Li(f"{round}: รับ {filtered_df[round].values[0]} คน") for round in tcas_rounds])
    else:
        tcas_intake_text = "กรุณาเลือกมหาวิทยาลัยและหลักสูตร"

    return tcas_intake_text

if __name__ == '__main__':
    app.run_server(debug=True)

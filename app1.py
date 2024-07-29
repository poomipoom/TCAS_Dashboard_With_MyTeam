import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go



import json
import re
# โหลดข้อมูล JSON
with open('tcas_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
# แปลงข้อมูล JSON เป็น DataFrame
df = pd.json_normalize(data)

# ข้อมูลลิสต์ของมหาวิทยาลัยและพิกัดละติจูด/ลองจิจูด
university_locations = {
    'จุฬาลงกรณ์มหาวิทยาลัย': {'latitude': 13.7463, 'longitude': 100.5320},
    'มหาวิทยาลัยเกษตรศาสตร์': {'latitude': 13.8500, 'longitude': 100.5584},
    'มหาวิทยาลัยกาฬสินธุ์': {'latitude': 15.5347, 'longitude': 103.4961},
    'มหาวิทยาลัยขอนแก่น': {'latitude': 16.4333, 'longitude': 102.8333},
    'มหาวิทยาลัยเชียงใหม่': {'latitude': 18.7874, 'longitude': 98.9934},
    'มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี': {'latitude': 13.7108, 'longitude': 100.5132},
    'มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ': {'latitude': 13.8592, 'longitude': 100.5120},
    'มหาวิทยาลัยทักษิณ': {'latitude': 7.0655, 'longitude': 100.5087},
    'มหาวิทยาลัยธรรมศาสตร์': {'latitude': 13.7652, 'longitude': 100.5558},
    'มหาวิทยาลัยนครพนม': {'latitude': 17.4206, 'longitude': 104.7230},
    'มหาวิทยาลัยนเรศวร': {'latitude': 16.8217, 'longitude': 100.5668},
    'มหาวิทยาลัยบูรพา': {'latitude': 12.9186, 'longitude': 100.9167},
    'มหาวิทยาลัยพะเยา': {'latitude': 19.1586, 'longitude': 99.8232},
    'มหาวิทยาลัยมหิดล': {'latitude': 13.7510, 'longitude': 100.5167},
    'มหาวิทยาลัยมหาสารคาม': {'latitude': 15.1833, 'longitude': 103.2833},
    'มหาวิทยาลัยรามคำแหง': {'latitude': 13.7846, 'longitude': 100.6242},
    'มหาวิทยาลัยศรีนครินทรวิโรฒ': {'latitude': 13.7678, 'longitude': 100.6201},
    'มหาวิทยาลัยศิลปากร': {'latitude': 13.7404, 'longitude': 100.2908},
    'มหาวิทยาลัยสงขลานครินทร์': {'latitude': 7.0070, 'longitude': 100.4640},
    'มหาวิทยาลัยอุบลราชธานี': {'latitude': 15.2800, 'longitude': 104.8711},
    'สถาบันเทคโนโลยีพระจอมเกล้าเจ้าคุณทหารลาดกระบัง': {'latitude': 13.7303, 'longitude': 100.7696},
    'มหาวิทยาลัยราชภัฏชัยภูมิ': {'latitude': 15.8120, 'longitude': 102.0360},
    'มหาวิทยาลัยราชภัฏบ้านสมเด็จเจ้าพระยา': {'latitude': 13.7333, 'longitude': 100.4833},
    'มหาวิทยาลัยราชภัฏสวนสุนันทา': {'latitude': 13.7750, 'longitude': 100.5510},
    'มหาวิทยาลัยเทคโนโลยีราชมงคลกรุงเทพ': {'latitude': 13.7540, 'longitude': 100.5014},
    'มหาวิทยาลัยเทคโนโลยีราชมงคลตะวันออก': {'latitude': 13.6762, 'longitude': 101.2914},
    'มหาวิทยาลัยเทคโนโลยีราชมงคลธัญบุรี': {'latitude': 13.9615, 'longitude': 100.6196},
    'มหาวิทยาลัยเทคโนโลยีราชมงคลรัตนโกสินทร์': {'latitude': 13.7600, 'longitude': 100.5140},
    'มหาวิทยาลัยเทคโนโลยีราชมงคลศรีวิชัย': {'latitude': 7.0060, 'longitude': 100.4680},
    'มหาวิทยาลัยเทคโนโลยีราชมงคลอีสาน': {'latitude': 15.0833, 'longitude': 104.8333},
    'มหาวิทยาลัยเกษมบัณฑิต': {'latitude': 13.8104, 'longitude': 100.5406},
    'มหาวิทยาลัยปทุมธานี': {'latitude': 14.0061, 'longitude': 100.4940},
    'มหาวิทยาลัยศรีปทุม': {'latitude': 13.9406, 'longitude': 100.5965},
    'มหาวิทยาลัยสยาม': {'latitude': 13.7411, 'longitude': 100.5282},
    'มหาวิทยาลัยหอการค้าไทย': {'latitude': 13.7490, 'longitude': 100.5776},
    'สถาบันการจัดการปัญญาภิวัฒน์': {'latitude': 13.7831, 'longitude': 100.5446}
}

# เพิ่มคอลัมน์ latitude และ longitude
df['latitude'] = df['university'].map(lambda x: university_locations.get(x, {}).get('latitude'))
df['longitude'] = df['university'].map(lambda x: university_locations.get(x, {}).get('longitude'))

# เปลี่ยนชื่อคอลัมน์
df.rename(columns={
    'intake_per_tcas_round.รอบ 1 Portfolio': 'Portfolio',
     'intake_per_tcas_round.รอบ 2 Quota': 'Quota',
       'intake_per_tcas_round.รอบ 3 Admission':'Admission',
       'intake_per_tcas_round.รอบ 4 Direct Admission': 'Direct Admission'
       # เปลี่ยนชื่อคอลัมน์ตามที่ต้องการ
}, inplace=True)


# ฟังก์ชันเพื่อทำการลบคำว่า 'รับ' และ 'คน' และแปลงเป็น int
def clean_and_convert(value):
    if value == "ไม่เปิดรับสมัครในรอบนี้":
        return 0
    else:
        # ลบคำว่า 'รับ' และ 'คน'
        value = value.replace('รับ ', '').replace(' คน', '')
        # แปลงเป็น int
        try:
            return int(value)
        except ValueError:
            return 0  # ถ้าแปลงไม่ได้ ให้คืนค่าเป็น 0
columns_to_clean = ['Portfolio', 'Quota', 'Admission', 'Direct Admission']
for col in columns_to_clean:
    df[col] = df[col].apply(clean_and_convert)
# คำนวณผลรวมของการรับสมัครจากทุกคอลัมน์
df['intake_per_course'] = df[columns_to_clean].sum(axis=1)

# ตรวจสอบ DataFrame หลังจากการอัปเดต
# print(df[['intake_per_course'] + columns_to_clean])


# การทำความสะอาดคอลัมน์ 'field'
df['field'] = df['field'].str.replace('.', '')  # ลบจุด
for i in range(0, 11):  # ลบตัวเลขจาก 1 ถึง 10
    df['field'] = df['field'].str.replace(str(i), '')

# ลบข้อความหลังเครื่องหมาย '(' ในคอลัมน์ 'program'
df['program'] = df['program'].apply(lambda x: x.split('(')[0].strip())
# การทำความสะอาดคอลัมน์ 'field'
df['program'] = df['program'].str.replace('.', '')  # ลบจุด
for i in range(0, 11):  # ลบตัวเลขจาก 1 ถึง 10
    df['program'] = df['program'].str.replace(str(i), '')


df['tuition_fee'] = df['tuition_fee'].apply(lambda x: x.split('หรือ')[0].strip())

def extract_amount(text):
    match = re.search(r'(\d{1,3}(?:,\d{3})*)', text)
    if match:
        return int(match.group(1).replace(',', ''))
    return None

def extract_tuition_fee(df):
    df['tuition_fee_amount'] = df['tuition_fee'].apply(extract_amount)
    df['term_or_course'] = df['tuition_fee'].apply(
        lambda x: 'per_term' if 'ภาคการศึกษา' in x else ('per_course' if 'ตลอดหลักสูตร' in x else 'unknown')
    )
    return df



df = extract_tuition_fee(df)
df['tuition_fee_amount'].fillna('N/A', inplace=True)
df = df.drop(columns=['faculty'])

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Engineering Programs Dashboard'),

    dcc.Tabs([
        dcc.Tab(label='Overview', children=[
            html.Div([
                html.H3('Program Overview'),
                dcc.Graph(
                    id='slots-bar-chart',
                    figure=px.bar(df, x='program', y='intake_per_course', title='Number of Slots per Program')
                ),
                dcc.Graph(
                    id='tuition-fee-bar-chart',
                    figure=px.bar(df, x='program', y='tuition_fee', title='Tuition Fee per Program')
                )
            ])
        ]),
        dcc.Tab(label='TCAS Rounds', children=[
            html.Div([
                dcc.Graph(
                    id='tcas-rounds-bar-chart',
                    figure=px.bar(df, x='program', y=['Portfolio', 'Quota'], title='TCAS Rounds Slots')
                )
            ])
        ]),
        dcc.Tab(label='Map', children=[
            html.Div([
                dcc.Graph(
                    id='map',
                    figure=go.Figure(go.Scattergeo(
                        lon=df['longitude'],
                        lat=df['latitude'],
                        text=df['university'],
                        mode='markers',
                        marker=dict(size=10, color='blue'),
                    )).update_layout(
                        title='University Locations',
                        geo=dict(
                            scope='asia',
                            showland=True
                        )
                    )
                )
            ])
        ])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)

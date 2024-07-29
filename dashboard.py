import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import json

# ข้อมูล
with open('tcas_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# แปลงข้อมูล JSON เป็น DataFrame
df = pd.json_normalize(data)
# ฟังก์ชันเพื่อแทนที่ค่า
def replace_not_accepted(d):
    return {k: (v if v != "ไม่เปิดรับสมัครในรอบนี้" else 0) for k, v in d.items()}


# ฟังก์ชันเพื่อทำการลบคำว่า 'รับ' และ 'คน' และแปลงเป็น int
def clean_and_convert_intake(d):
    cleaned = {}
    for k, v in d.items():
        if v == "ไม่เปิดรับสมัครในรอบนี้":
            cleaned[k] = v
        else:
            # ลบคำว่า 'รับ' และ 'คน'
            value = v.replace('รับ ', '').replace(' คน', '')
            # แปลงเป็น int
            cleaned[k] = int(value)
    return cleaned

# ใช้ฟังก์ชันกับคอลัมน์
df['intake_per_tcas_round'] = df['intake_per_tcas_round'].apply(clean_and_convert_intake)
df['intake_per_tcas_round'] = df['intake_per_tcas_round'].apply(replace_not_accepted)
# Streamlit App
st.title('Dashboard ข้อมูลหลักสูตรวิศวกรรม')

# แสดงข้อมูลทั้งหมด
st.subheader('ข้อมูลหลักสูตร')
st.write(df)

# สร้างกราฟแท่งแสดงจำนวนรับตามรอบ TCAS
st.subheader('จำนวนรับตามรอบ TCAS')
for index, row in df.iterrows():
    rounds = list(row['intake_per_tcas_round'].keys())
    values = list(row['intake_per_tcas_round'].values())

    fig = go.Figure([go.Bar(x=rounds, y=values)])
    fig.update_layout(title=row['program'], xaxis_title='รอบ TCAS', yaxis_title='จำนวนรับ')
    st.plotly_chart(fig)

# สร้างกราฟวงกลมแสดงค่าธรรมเนียมการเรียน
st.subheader('ค่าธรรมเนียมการเรียน')
tuition_fees = {
    "ค่าธรรมเนียมภาคการศึกษาต้นและปลาย": 25500,
    "ค่าธรรมเนียมภาคฤดูร้อน": 6375
}
fig2 = go.Figure([go.Pie(labels=list(tuition_fees.keys()), values=list(tuition_fees.values()))])
fig2.update_layout(title='ค่าธรรมเนียมการเรียน')
st.plotly_chart(fig2)

# แสดงข้อมูลวิทยาเขต
st.subheader('วิทยาเขต')
campus_counts = df['campus'].value_counts()
fig3 = go.Figure([go.Bar(x=campus_counts.index, y=campus_counts.values)])
fig3.update_layout(title='จำนวนหลักสูตรตามวิทยาเขต', xaxis_title='วิทยาเขต', yaxis_title='จำนวนหลักสูตร')
st.plotly_chart(fig3)

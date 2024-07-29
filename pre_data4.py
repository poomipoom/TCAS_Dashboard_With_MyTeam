

import json
import pandas as pd
import re
# โหลดข้อมูล JSON
with open('tcas_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
# แปลงข้อมูล JSON เป็น DataFrame
df = pd.json_normalize(data)


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
print(df)
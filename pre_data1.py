import pandas as pd
import json

# โหลดข้อมูล JSON
with open('tcas_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# แปลงข้อมูล JSON เป็น DataFrame
df = pd.json_normalize(data)

# ลบข้อความหลังเครื่องหมาย '(' ในคอลัมน์ 'program'
df['program'] = df['program'].apply(lambda x: x.split('(')[0].strip())

# ลบหลักสูตรที่ซ้ำกันออก
unique_programs = df['program'].drop_duplicates()

# แสดงผลหลักสูตรที่ไม่ซ้ำกัน
for program in unique_programs:
    print(program)

# สร้าง DataFrame ที่มีหลักสูตรที่ไม่ซ้ำกัน
unique_programs_df = unique_programs.reset_index(drop=True)

# แสดง DataFrame
print(unique_programs_df)

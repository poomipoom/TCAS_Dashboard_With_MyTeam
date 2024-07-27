import json
import re
import pandas as pd
# โหลดข้อมูล JSON
with open('data/tcas_data2.json', 'r', encoding='utf-8') as file:
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
    'สถาบันการจัดการปัญญาภิวัฒน์': {'latitude': 13.7831, 'longitude': 100.5446},
    'มหาวิทยาลัยเทคโนโลยีสุรนารี': {'latitude': 14.8819, 'longitude': 102.0155},
    'มหาวิทยาลัยนราธิวาสราชนครินทร์': {'latitude': 6.4264, 'longitude': 101.8233},
    'มหาวิทยาลัยวลัยลักษณ์': {'latitude': 8.6478, 'longitude': 99.8907},
    'มหาวิทยาลัยราชภัฏเพชรบุรี': {'latitude': 13.1122, 'longitude': 99.9461},
    'มหาวิทยาลัยรังสิต': {'latitude': 13.9625, 'longitude': 100.5886},
    'มหาวิทยาลัยเทคโนโลยีมหานคร': {'latitude': 13.8151, 'longitude': 100.6803},
    'มหาวิทยาลัยแม่โจ้': {'latitude': 18.8898, 'longitude': 99.0200},
    'มหาวิทยาลัยธุรกิจบัณฑิตย์': {'latitude': 13.8653, 'longitude': 100.5344}
    

}

# ข้อมูลที่ต้องการเพิ่ม
data_to_add = [
    {"university": "จุฬาลงกรณ์มหาวิทยาลัย", "campus": "วิทยาเขตหลัก"},
    {"university": "มหาวิทยาลัยเกษตรศาสตร์", "campus": "วิทยาเขตหลัก"},
    {"university": "มหาวิทยาลัยเกษตรศาสตร์", "campus": "บางเขน"},
    {"university": "มหาวิทยาลัยเกษตรศาสตร์", "campus": "กำแพงแสน"},
    {"university": "มหาวิทยาลัยเกษตรศาสตร์", "campus": "ศรีราชา"},
    {"university": "มหาวิทยาลัยเกษตรศาสตร์", "campus": "เฉลิมพระเกียรติ จ.สกลนคร"},
    {"university": "มหาวิทยาลัยขอนแก่น", "campus": "ขอนแก่น"},
    {"university": "มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี", "campus": "บางมด"},
    {"university": "มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ", "campus": "กรุงเทพฯ"},
    {"university": "มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ", "campus": "ปราจีนบุรี"},
    {"university": "มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ", "campus": "ระยอง"},
    {"university": "มหาวิทยาลัยทักษิณ", "campus": "พัทลุง"},
    {"university": "มหาวิทยาลัยธรรมศาสตร์", "campus": "ศูนย์รังสิต"},
    {"university": "มหาวิทยาลัยธรรมศาสตร์", "campus": "ศูนย์พัทยา"},
    {"university": "มหาวิทยาลัยบูรพา", "campus": "หลัก"},
    {"university": "มหาวิทยาลัยมหิดล", "campus": "ศาลายา"},
    {"university": "มหาวิทยาลัยมหาสารคาม", "campus": "มหาสารคาม"},
    {"university": "มหาวิทยาลัยแม่โจ้", "campus": "วิทยาเขตเชียงใหม่"},
    {"university": "มหาวิทยาลัยรามคำแหง", "campus": "วิทยาเขตหลักหัวหมาก"},
    {"university": "มหาวิทยาลัยศรีนครินทรวิโรฒ", "campus": "องครักษ์"},
    {"university": "มหาวิทยาลัยศิลปากร", "campus": "สนามจันทร์"},
    {"university": "มหาวิทยาลัยสงขลานครินทร์", "campus": "หาดใหญ่"},
    {"university": "สถาบันเทคโนโลยีพระจอมเกล้าเจ้าคุณทหารลาดกระบัง", "campus": "ลาดกระบัง"},
    {"university": "มหาวิทยาลัยเทคโนโลยีราชมงคลตะวันออก", "campus": "คณะ/สถาบันในส่วนกลาง"},
    {"university": "มหาวิทยาลัยเทคโนโลยีราชมงคลตะวันออก", "campus": "วิทยาเขตจันทบุรี"},
    {"university": "มหาวิทยาลัยเทคโนโลยีราชมงคลตะวันออก", "campus": "วิทยาเขตอุเทนถวาย"},
    {"university": "มหาวิทยาลัยเทคโนโลยีราชมงคลรัตนโกสินทร์", "campus": "วังไกลกังวล"},
    {"university": "มหาวิทยาลัยเทคโนโลยีราชมงคลศรีวิชัย", "campus": "สงขลา"},
    {"university": "มหาวิทยาลัยเทคโนโลยีราชมงคลศรีวิชัย", "campus": "ตรัง"},
    {"university": "มหาวิทยาลัยเทคโนโลยีราชมงคลอีสาน", "campus": "นครราชสีมา"},
    {"university": "มหาวิทยาลัยเกษมบัณฑิต", "campus": "วิทยาเขตพัฒนาการ"},
    {"university": "มหาวิทยาลัยเกษมบัณฑิต", "campus": "วิทยาเขตร่มเกล้า"},
    {"university": "สถาบันการจัดการปัญญาภิวัฒน์", "campus": "แจ้งวัฒนะ นนทบุรี"},
    {"university": "สถาบันการจัดการปัญญาภิวัฒน์", "campus": "อีอีซี"}
]

# ข้อมูลพิกัดของแต่ละวิทยาเขต
campus_locations = {
    'วิทยาเขตหลัก': {'latitude': 13.7463, 'longitude': 100.5320},
    'บางเขน': {'latitude': 13.8500, 'longitude': 100.5584},
    'กำแพงแสน': {'latitude': 14.0401, 'longitude': 99.9546},
    'ศรีราชา': {'latitude': 13.1914, 'longitude': 101.2952},
    'เฉลิมพระเกียรติ จ.สกลนคร': {'latitude': 17.1622, 'longitude': 104.1722},
    'ขอนแก่น': {'latitude': 16.4333, 'longitude': 102.8333},
    'บางมด': {'latitude': 13.7108, 'longitude': 100.5132},
    'กรุงเทพฯ': {'latitude': 13.8592, 'longitude': 100.5120},
    'ปราจีนบุรี': {'latitude': 13.9406, 'longitude': 101.3482},
    'ระยอง': {'latitude': 12.6792, 'longitude': 101.2707},
    'พัทลุง': {'latitude': 7.0655, 'longitude': 100.5087},
    'ศูนย์รังสิต': {'latitude': 13.7652, 'longitude': 100.5558},
    'ศูนย์พัทยา': {'latitude': 12.9278, 'longitude': 100.8970},
    'หลัก': {'latitude': 12.9186, 'longitude': 100.9167},
    'ศาลายา': {'latitude': 13.7510, 'longitude': 100.5167},
    'มหาสารคาม': {'latitude': 15.1833, 'longitude': 103.2833},
    'วิทยาเขตเชียงใหม่': {'latitude': 18.7874, 'longitude': 98.9934},
    'วิทยาเขตหลักหัวหมาก': {'latitude': 13.7846, 'longitude': 100.6242},
    'องครักษ์': {'latitude': 13.7678, 'longitude': 100.6201},
    'สนามจันทร์': {'latitude': 13.7404, 'longitude': 100.2908},
    'หาดใหญ่': {'latitude': 7.0070, 'longitude': 100.4640},
    'ลาดกระบัง': {'latitude': 13.7303, 'longitude': 100.7696},
    'คณะ/สถาบันในส่วนกลาง': {'latitude': 13.7540, 'longitude': 100.5014},
    'วิทยาเขตจันทบุรี': {'latitude': 12.6031, 'longitude': 102.1091},
    'วิทยาเขตอุเทนถวาย': {'latitude': 13.8461, 'longitude': 100.5361},
    'วังไกลกังวล': {'latitude': 13.8000, 'longitude': 100.5710},
    'สงขลา': {'latitude': 7.0070, 'longitude': 100.4640},
    'ตรัง': {'latitude': 7.5536, 'longitude': 99.6117},
    'นครราชสีมา': {'latitude': 15.0833, 'longitude': 104.8333},
    'วิทยาเขตพัฒนาการ': {'latitude': 13.8104, 'longitude': 100.5406},
    'วิทยาเขตร่มเกล้า': {'latitude': 13.8104, 'longitude': 100.5406},
    'แจ้งวัฒนะ นนทบุรี': {'latitude': 13.8720, 'longitude': 100.5087},
    'อีอีซี': {'latitude': 13.8720, 'longitude': 100.5087}
}

df_1 = pd.DataFrame(data_to_add)
# เพิ่มพิกัด lat long ลงใน DataFrame
df['latitude'] = df['campus'].map(lambda x: campus_locations.get(x, {}).get('latitude', None))
df['longitude'] = df['campus'].map(lambda x: campus_locations.get(x, {}).get('longitude', None))

print(df)


# # เพิ่มคอลัมน์ latitude และ longitude
# df['latitude'] = df['university'].map(lambda x: university_locations.get(x, {}).get('latitude'))
# df['longitude'] = df['university'].map(lambda x: university_locations.get(x, {}).get('longitude'))

df

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
# df['program'] = df['program'].apply(lambda x: x.split('(')[0].strip())
# การทำความสะอาดคอลัมน์ 'field'
df['program'] = df['program'].str.replace('.', '')  # ลบจุด
df['program'] = df['program'].str.replace('วศบ', 'วิศวกรรมศาสตรบัณฑิต')
df['program'] = df['program'].str.replace('วทบ', 'วิทยาศาสตรบัณฑิต')
  # ลบจุด
for i in range(0, 11):  # ลบตัวเลขจาก 1 ถึง 10
    df['program'] = df['program'].str.replace(str(i), '')


df['tuition_fee'] = df['tuition_fee'].apply(lambda x: x.split('หรือ')[0].strip())

def extract_amount(text):
    match = re.search(r'(\d{1,3}(?:,\d{3})*)', text)
    if match:
        return int(match.group(1).replace(',', ''))
    return None

def extract_tuition_fee(df):
    # df['tuition_fee_amount'] = df['tuition_fee'].apply(extract_amount)
    df['tuition_fee_amount'] = df['tuition_fee'].apply(extract_amount)
    # df['term_or_course'] = df['tuition_fee'].apply(
    #     lambda x: 'per_term' if 'ภาค' in x else ('per_course' if 'ตลอดหลักสูตร' in x else 'unknown')
    # )
    # df['term_or_course'] = df['tuition_fee'].apply(
    #     lambda x: 'per_term' if 'ภาค' in x else ('per_term' if 'เหมา' in x else 'unknown')
    # )
    # df['term_or_course'] = df['tuition_fee'].apply(
    #     lambda x: 'per_term' if 'เทอม' in x else ('per_term' if 'เหมา' in x else 'unknown')
    # )
    df['term_or_course'] = df['tuition_fee'].apply(
        lambda x: 'per_term' if 'ภาค' in x else ('per_course' if 'ตลอดหลักสูตร' in x else ('per_term' if 'เทอม' in x else 'unknown'))
    )
    
    return df

# ฟังก์ชันเพื่อตรวจสอบและเพิ่มข้อความ "ค่าใช้จ่ายตลอดหลักสูตร" หรือ "ค่าใช้จ่ายต่อเทอม"
def add_course_fee_prefix(value):
    # ลบเครื่องหมายจุลภาคออก
    value_cleaned = value.replace(',', '')
    
    try:
        check_v = int(value_cleaned)
    except ValueError:
        return value
    
    if check_v > 20000:
        if re.match(r'^\d+(,\d{3})*$', value):
            return f"ค่าใช้จ่ายตลอดหลักสูตร {value}"
    else:
        if re.match(r'^\d+(,\d{3})*$', value):
            return f"ค่าใช้จ่ายต่อเทอม {value}"
    
    return value

# ใช้ฟังก์ชันกับคอลัมน์ 'tuition_fee'
df['tuition_fee'] = df['tuition_fee'].apply(add_course_fee_prefix)

# ตรวจสอบ DataFrame หลังจากการอัปเดต
print(df['tuition_fee'])

df = extract_tuition_fee(df)
df['tuition_fee_amount'] = df['tuition_fee_amount'].astype(str)
df['tuition_fee_amount'] = df['tuition_fee_amount'].fillna('N/A')
# df['tuition_fee_amount'] = df['tuition_fee_amount'].astype(int)

# กรอง DataFrame ให้เก็บเฉพาะแถวที่มีคำว่า "วิศวกรรม" อยู่ในคอลัมน์ 'field'
df = df[df['field'].str.contains('วิศวกรรม')]

df['program'] = df['program'].apply(lambda x: x.split('วิทยาเขต')[0].strip())
df['program'] = df['program'].str.replace('(หลักสูตรนานาชาติ)', '')
df['program'] = df['program'].str.replace('หลักสูตร', '')
df['program'] = df['program'].str.replace('วิศวกรรมศาสตรบัณฑิต', 'หลักสูตรวิศวกรรมศาสตรบัณฑิต ')
df['program'] = df['program'].str.replace('(หลักสูตรวิศวกรรมศาสตรบัณฑิต )', '')
# df['program'] = df['program'].str.replace('(วิศวกรรมโลจิสติกส์ )', '')





df = df.drop(columns=['faculty'])

# print(df['field'].unique())
# print(df['program'].unique())
# ใช้ drop_duplicates() เพื่อลบค่า campus ที่ซ้ำ
unique_campus_df = df.drop_duplicates(subset=['campus'])

unique_campus_df = unique_campus_df[['university','campus']]
print(unique_campus_df)


# campus_dict = unique_campus_df.to_dict(orient='records')
# # บันทึก Dictionary เป็นไฟล์ JSON
# with open('data/campus.json', 'w', encoding='utf-8') as f:
#     json.dump(campus_dict, f, ensure_ascii=False, indent=4)



# แปลง DataFrame เป็น Dictionary
data_dict = df.to_dict(orient='records')

# บันทึก Dictionary เป็นไฟล์ JSON
with open('data/data3.json', 'w', encoding='utf-8') as f:
    json.dump(data_dict, f, ensure_ascii=False, indent=4)
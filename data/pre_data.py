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

campus_locations=[
    {"university": "มหาวิทยาลัยเกษตรศาสตร์", "campus": "บางเขน", "latitude": 13.847860, "longitude": 100.571247},
    {"university": "มหาวิทยาลัยเกษตรศาสตร์", "campus": "กำแพงแสน", "latitude": 14.022632, "longitude": 99.973322},
    {"university": "มหาวิทยาลัยเกษตรศาสตร์", "campus": "ศรีราชา", "latitude": 13.169799, "longitude": 100.926673},
    {"university": "มหาวิทยาลัยเกษตรศาสตร์", "campus": "เฉลิมพระเกียรติ จ.สกลนคร", "latitude": 17.227358, "longitude": 104.120297},
    {"university": "มหาวิทยาลัยขอนแก่น", "campus": "ขอนแก่น", "latitude": 16.472894, "longitude": 102.823721},
    {"university": "มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี", "campus": "บางมด", "latitude": 13.651245, "longitude": 100.494220},
    {"university": "มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ", "campus": "กรุงเทพฯ", "latitude": 13.820587, "longitude": 100.513390},
    {"university": "มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ", "campus": "ปราจีนบุรี", "latitude": 14.044907, "longitude": 101.373805},
    {"university": "มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ", "campus": "ระยอง", "latitude": 12.708049, "longitude": 101.159537},
    {"university": "มหาวิทยาลัยทักษิณ", "campus": "พัทลุง", "latitude": 7.616124, "longitude": 100.083171},
    {"university": "มหาวิทยาลัยธรรมศาสตร์", "campus": "ศูนย์รังสิต", "latitude": 14.066973, "longitude": 100.607818},
    {"university": "มหาวิทยาลัยธรรมศาสตร์", "campus": "ศูนย์พัทยา", "latitude": 12.959155, "longitude": 100.901372},
    {"university": "มหาวิทยาลัยบูรพา", "campus": "หลัก", "latitude": 13.284362, "longitude": 100.926741},
    {"university": "มหาวิทยาลัยมหิดล", "campus": "ศาลายา", "latitude": 13.793455, "longitude": 100.325550},
    {"university": "มหาวิทยาลัยมหาสารคาม", "campus": "มหาสารคาม", "latitude": 16.245403, "longitude": 103.252396},
    {"university": "มหาวิทยาลัยแม่โจ้", "campus": "วิทยาเขตเชียงใหม่", "latitude": 18.897318, "longitude": 99.016948},
    {"university": "มหาวิทยาลัยรามคำแหง", "campus": "วิทยาเขตหลักหัวหมาก", "latitude": 13.759892, "longitude": 100.625821},
    {"university": "มหาวิทยาลัยศรีนครินทรวิโรฒ", "campus": "องครักษ์", "latitude": 14.076735, "longitude": 101.378024},
    {"university": "มหาวิทยาลัยศิลปากร", "campus": "สนามจันทร์", "latitude": 13.817545, "longitude": 100.041840},
    {"university": "มหาวิทยาลัยสงขลานครินทร์", "campus": "หาดใหญ่", "latitude": 7.006761, "longitude": 100.498247},
    {"university": "สถาบันเทคโนโลยีพระจอมเกล้าเจ้าคุณทหารลาดกระบัง", "campus": "ลาดกระบัง", "latitude": 13.729039, "longitude": 100.779978},
    {"university": "มหาวิทยาลัยเทคโนโลยีราชมงคลตะวันออก", "campus": "คณะ/สถาบันในส่วนกลาง", "latitude": 13.153211, "longitude": 101.136255},
    {"university": "มหาวิทยาลัยเทคโนโลยีราชมงคลตะวันออก", "campus": "วิทยาเขตจันทบุรี", "latitude": 12.618932, "longitude": 102.104781},
    {"university": "มหาวิทยาลัยเทคโนโลยีราชมงคลตะวันออก", "campus": "วิทยาเขตอุเทนถวาย", "latitude": 13.745058, "longitude": 100.529870},
    {"university": "มหาวิทยาลัยเทคโนโลยีราชมงคลรัตนโกสินทร์", "campus": "วังไกลกังวล", "latitude": 12.558940, "longitude": 99.962772},
    {"university": "มหาวิทยาลัยเทคโนโลยีราชมงคลศรีวิชัย", "campus": "สงขลา", "latitude": 7.171045, "longitude": 100.611430},
    {"university": "มหาวิทยาลัยเทคโนโลยีราชมงคลศรีวิชัย", "campus": "ตรัง", "latitude": 7.484013, "longitude": 99.624722},
    {"university": "มหาวิทยาลัยเทคโนโลยีราชมงคลอีสาน", "campus": "นครราชสีมา", "latitude": 14.980378, "longitude": 102.100576},
    {"university": "มหาวิทยาลัยเกษมบัณฑิต", "campus": "วิทยาเขตพัฒนาการ", "latitude": 13.732402, "longitude": 100.647618},
    {"university": "มหาวิทยาลัยเกษมบัณฑิต", "campus": "วิทยาเขตร่มเกล้า", "latitude": 13.773926, "longitude": 100.747507},
    {"university": "สถาบันการจัดการปัญญาภิวัฒน์", "campus": "แจ้งวัฒนะ นนทบุรี", "latitude": 13.896657, "longitude": 100.528891},
    {"university": "สถาบันการจัดการปัญญาภิวัฒน์", "campus": "อีอีซี", "latitude": 12.955797, "longitude": 100.891847}
]


# เพิ่มคอลัมน์ latitude และ longitude
def get_latitude(university, campus):
    # ค้นหาวิทยาเขตที่ตรงกัน
    for location in campus_locations:
        if location['university'] == university and location['campus'] == campus:
            return location['latitude']
    # ถ้าไม่พบวิทยาเขตที่ตรงกัน ให้คืนค่าละติจูดของมหาวิทยาลัย
    return university_locations.get(university, {}).get('latitude')

def get_longitude(university, campus):
    # ค้นหาวิทยาเขตที่ตรงกัน
    for location in campus_locations:
        if location['university'] == university and location['campus'] == campus:
            return location['longitude']
    # ถ้าไม่พบวิทยาเขตที่ตรงกัน ให้คืนค่าลองจิจูดของมหาวิทยาลัย
    return university_locations.get(university, {}).get('longitude')

df['latitude'] = df.apply(lambda row: get_latitude(row['university'], row['campus']), axis=1)
df['longitude'] = df.apply(lambda row: get_longitude(row['university'], row['campus']), axis=1)





# df

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




# การทำความสะอาดคอลัมน์ 'field'
df['field'] = df['field'].str.replace('.', '')  # ลบจุด
for i in range(0, 11):  # ลบตัวเลขจาก 1 ถึง 10
    df['field'] = df['field'].str.replace(str(i), '')

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
    df['tuition_fee_amount'] = df['tuition_fee'].apply(extract_amount)
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

# กรอง DataFrame ให้เก็บเฉพาะแถวที่มีคำว่า "วิศวกรรม" อยู่ในคอลัมน์ 'field'
df = df[df['field'].str.contains('วิศวกรรม')]

df['program'] = df['program'].apply(lambda x: x.split('วิทยาเขต')[0].strip())
df['program'] = df['program'].str.replace('(หลักสูตรนานาชาติ)', '')
df['program'] = df['program'].str.replace('หลักสูตร', '')
df['program'] = df['program'].str.replace('วิศวกรรมศาสตรบัณฑิต', 'หลักสูตรวิศวกรรมศาสตรบัณฑิต ')
df['program'] = df['program'].str.replace('(หลักสูตรวิศวกรรมศาสตรบัณฑิต )', '')






df = df.drop(columns=['faculty'])

# box = df['campus'].replace('วิทยาเขตหลัก','').unique()

# print(box)
df['tuition_fee'] = df['tuition_fee'].apply(lambda x: x.split('ดูราย')[0].strip())
df['tuition_fee'] = df['tuition_fee'].replace('', 'N/A')

df['tuition_fee'] = df['tuition_fee'].str.replace('N/A', 'ไม่ได้ระบุ')
# df['tuition_fee'] = df['tuition_fee'].fillna('N/A')

# df.loc[df['field'].str.strip() == 'วิศวกรรมทั่วไป', 'program'] = 'หลักสูตรวิศวกรรมศาสตรบัณฑิต วิศวกรรมศาสตร์ (ภาษาไทย ปกติ)'
print(df.loc[df['field'].str.strip() == 'วิศวกรรมทั่วไป', 'program'].unique())
# แก้ไขค่าในคอลัมน์ 'program' ตามเงื่อนไขที่กำหนด
df.loc[
    (df['field'].str.strip() == 'วิศวกรรมทั่วไป') & 
    (df['program'].str.contains('(ภาษาไทย ปกติ)')),
    'program'
] = 'หลักสูตรวิศวกรรมศาสตรบัณฑิต วิศวกรรมศาสตร์ (ภาษาไทย ปกติ)'



print(df['program'].nunique())
# print(normalized_programs,df['program'].unique())
df['program'] = df['program'].str.replace('สาขาวิชา', '')
df['program'] = df['program'].str.replace('หลักสูตรวิศวกรรมศาสตรบัณฑิต  ', 'หลักสูตรวิศวกรรมศาสตรบัณฑิต ')


# แปลง DataFrame เป็น Dictionary
data_dict = df.to_dict(orient='records')

# บันทึก Dictionary เป็นไฟล์ JSON
with open('data/data3.json', 'w', encoding='utf-8') as f:
    json.dump(data_dict, f, ensure_ascii=False, indent=4)
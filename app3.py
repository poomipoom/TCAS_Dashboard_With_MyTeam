from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# ตั้งค่า WebDriver (สมมติใช้ ChromeDriver)
# driver_path = 'path_to_chromedriver'  # เปลี่ยนเป็นเส้นทางที่ถูกต้องของ ChromeDriver ในเครื่องคุณ
driver = webdriver.Chrome()

# เปิดเว็บไซต์ MyTCAS
driver.get('https://www.mytcas.com/universities/')

# รอให้หน้าเว็บโหลดเสร็จ
time.sleep(5)  # ปรับเวลาให้เหมาะสมกับการโหลดหน้าเว็บ

# ดึงข้อมูลรายชื่อมหาวิทยาลัย
universities = []

try:
    # ค้นหาองค์ประกอบที่เป็นรายการมหาวิทยาลัย
    university_elements = driver.find_elements(By.CSS_SELECTOR, '.u-list .unv-list .brand')

    for university in university_elements:
        name = university.text
        link = university.get_attribute('href')
        universities.append({'name': name, 'link': link})

except Exception as e:
    print(f"เกิดข้อผิดพลาด: {e}")

finally:
    # ปิด WebDriver
    driver.quit()

# แสดงข้อมูลรายชื่อมหาวิทยาลัย
for university in universities:
    print(f"Name: {university['name']}")
    print(f"Link: {university['link']}")
    print("-" * 30)

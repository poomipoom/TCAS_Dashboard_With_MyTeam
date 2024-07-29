from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome()
# เปิดหน้าเว็บ
driver.get('https://course.mytcas.com/universities/')

# รอให้เนื้อหาจาก JavaScript โหลด
driver.implicitly_wait(10)  # รอไม่เกิน 10 วินาที

try:
    a_tags = driver.find_elements(By.CSS_SELECTOR, 'a.brand')
    for a_tag in a_tags:
        university_name = a_tag.text
        # ดึง URL ของลิงก์
        link_url = a_tag.get_attribute('href')
        img_tag = a_tag.find_element(By.TAG_NAME, 'img')
        logo_url = img_tag.get_attribute('src') if img_tag else 'No image'
        
        print(f'University Name: {university_name}')
        print(f'Link URL: {link_url}')
        print(f'Logo URL: {logo_url}')
finally:
    driver.quit()

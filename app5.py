from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome()


def extract_university_data():
    # เปิดหน้าเว็บหลักที่มีลิงก์ของแต่ละสถาบัน
    driver.get('https://course.mytcas.com/universities/')
    
    # รอให้อิลิเมนต์ <a> ที่มีคลาส 'brand' โหลดเสร็จ
    wait = WebDriverWait(driver, 10)
    a_tags = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.brand')))
    
    university_data = []

    try:
        for a_tag in a_tags:
            university_name = a_tag.text
            link_url = a_tag.get_attribute('href')
            img_tag = a_tag.find_element(By.TAG_NAME, 'img')
            logo_url = img_tag.get_attribute('src') if img_tag else 'No image'
            
            # ไปที่ลิงก์ของแต่ละสถาบัน
            driver.get(link_url)
            
            # รอให้อิลิเมนต์คณะโหลดเสร็จ
            faculty_tags = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href^="/universities/"][href*="/faculties/"]')))
            faculties = []
            for faculty_tag in faculty_tags:
                faculty_name = faculty_tag.text
                faculty_link = faculty_tag.get_attribute('href')
                faculties.append({'name': faculty_name, 'link': faculty_link})
            
            # เก็บข้อมูลทั้งหมด
            if faculties:  # เก็บข้อมูลเฉพาะสถาบันที่มีคณะวิศวกรรม
                university_data.append({
                    'University Name': university_name,
                    'Link URL': link_url,
                    'Logo URL': logo_url,
                    'Faculties': faculties
                })
    finally:
        driver.quit()
    
    return university_data

def main():
    data = extract_university_data()
    for university in data:
        print(f"University Name: {university['University Name']}")
        print(f"Link URL: {university['Link URL']}")
        print(f"Logo URL: {university['Logo URL']}")
        print("Faculties:")
        for faculty in university['Faculties']:
            print(f"  Name: {faculty['name']}")
            print(f"  Link: {faculty['link']}")
        print("\n")

if __name__ == "__main__":
    main()
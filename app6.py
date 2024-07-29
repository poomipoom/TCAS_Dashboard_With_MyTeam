from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

def check_university_links():
    # เปิดหน้าเว็บหลักที่มีลิงก์ของแต่ละสถาบัน
    driver.get('https://course.mytcas.com/universities/')
    
    # รอให้อิลิเมนต์ <a> ที่มีคลาส 'brand' โหลดเสร็จ
    wait = WebDriverWait(driver, 10)
    a_tags = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.brand')))
    
    try:
        for a_tag in a_tags:
            university_name = a_tag.text
            link_url = a_tag.get_attribute('href')
            
            # ไปที่ลิงก์ของแต่ละสถาบัน
            driver.get(link_url)
            
            # ตรวจสอบว่ามาถึงหน้าใหม่ได้หรือไม่
            print(f"Successfully accessed {university_name} at {link_url}")

             # Wait for faculty links to load
            try:
                faculty_links = wait.until(EC.presence_of_all_elements_located(
                    (By.PARTIAL_LINK_TEXT, 'วิศวกรรม')
                ))
                
                print(f"University: {university_name}")
                
                # Print faculty links that contain "วิศวกรรม"
                for faculty_link in faculty_links:
                    faculty_name = faculty_link.text
                    faculty_url = faculty_link.get_attribute('href')
                    print(f"  Faculty: {faculty_name} - {faculty_url}")
            except Exception as e:
                print(f"Error fetching faculties for {university_name}: {str(e)}")
                
        


            
            # สามารถเพิ่มการรอหรือการตรวจสอบเพิ่มเติมได้ที่นี่
            # เช่น รอให้บางส่วนของหน้าโหลดเสร็จ

            # กลับไปยังหน้าเว็บหลัก
            driver.back()
            
    finally:
        driver.quit()

def main():
    check_university_links()

if __name__ == "__main__":
    main()

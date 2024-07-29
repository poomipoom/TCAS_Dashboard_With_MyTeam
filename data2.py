from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless Chrome
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the Chrome driver
driver = webdriver.Chrome(options=chrome_options)
def extract_program_details(url):
    driver.get(url)
    wait = WebDriverWait(driver, 2)
    
    details = {}
    
    try:
        dt_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'dl dt')))
        dd_elements = driver.find_elements(By.CSS_SELECTOR, 'dl dd')

        for dt, dd in zip(dt_elements, dd_elements):
            dt_text = dt.text.strip()
            dd_text = dd.text.strip()
            
            if dt_text:
                details[dt_text] = dd_text
        
        return details
    
    except Exception as e:
        print(f"An error occurred while extracting details: {e}")
        return None

def collect_data():
    all_data = []

    try:
        driver.get('https://course.mytcas.com/universities/')
        wait = WebDriverWait(driver, 10)

        a_tags = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.brand')))
        university_links = [(a.text, a.get_attribute('href')) for a in a_tags]

        for university_name, link_url in university_links:
            try:
                print(f"Successfully accessed {university_name} at {link_url}")

                driver.get(link_url)
                # time.sleep(0.001)

                faculty_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href^="/universities/"][href*="/faculties/"]')))
                faculty_links_filtered = [(fl.get_attribute('innerText').strip(), fl.get_attribute('href')) 
                                          for fl in faculty_links if "วิศวกรรม" in fl.get_attribute('innerText').strip()]

                for faculty_name, faculty_url in faculty_links_filtered:
                    try:
                        print(f"Successfully accessed {faculty_name} at {faculty_url}")

                        driver.get(faculty_url)
                        # time.sleep(0.001)

                        field_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href*="/fields/"]')))
                        field_links = [(field.get_attribute('innerText').strip(), field.get_attribute('href')) for field in field_links]
                        
                        for field_name, field_url in field_links:
                            try:
                                print(f"Successfully accessed {field_name} at {field_url}")
                                driver.get(field_url)
                                # time.sleep(0.001)
                                
                                # Retrieve and process all program links for the field
                                program_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href*="/programs/"]')))
                                program_links = [(program.get_attribute('text'),program.get_attribute('href')) for program in program_links]
                            
                                for program_name, program_url in program_links:
                                    try:
                                        print(f"Successfully accessed {program_name} at {program_url}")
                                        # time.sleep(0.001)
                                        program_details = extract_program_details(program_url)
                                        if program_details:
                                            intake_per_course = program_details.get('จำนวนรับ', 'N/A')
                                            intake_per_tcas_round = {key: value for key, value in program_details.items() if "รอบ" in key}
                                            tuition_fee = program_details.get('ค่าใช้จ่าย', 'N/A')
                                            campus = program_details.get('วิทยาเขต', 'N/A')
                                            success_percentage = program_details.get('อัตราการสำเร็จการศึกษา', 'N/A')
                                            
                                            print("Program Details:")
                                            for key, value in program_details.items():
                                                print(f"      {key}: {value}")

                                            all_data.append({
                                                'university': university_name,
                                                'faculty': faculty_name,
                                                'field': field_name,
                                                'program': program_name,
                                                'intake_per_course': intake_per_course,
                                                'intake_per_tcas_round': intake_per_tcas_round,
                                                'tuition_fee': tuition_fee,
                                                'campus': campus,
                                                'success_percentage':success_percentage,
                                            })
                                    except StaleElementReferenceException:
                                        print("Stale element reference exception occurred for program link.")
                                        continue

                                driver.back()  # Go back to field page
                                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href*="/programs/"]')))

                            except StaleElementReferenceException:
                                print("Stale element reference exception occurred for field link.")
                                continue

                        driver.back()  # Go back to faculty page
                        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href*="/fields/"]')))

                    except StaleElementReferenceException:
                        print("Stale element reference exception occurred for faculty link.")
                        continue

            except TimeoutException:
                print(f"Timeout when accessing {university_name} at {link_url}.")
                continue
            except StaleElementReferenceException:
                print("Stale element reference exception occurred for university link.")
                continue

    finally:
        driver.quit()
    
    return all_data

# Collect the data
collected_data = collect_data()

# Save data to JSON file
with open('tcas_data2.json', 'w', encoding='utf-8') as f:
    json.dump(collected_data, f, ensure_ascii=False, indent=4)

print("Data collection complete. Data saved to 'tcas_data.json'.")

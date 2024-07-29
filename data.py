import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless Chrome
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the Chrome driver
driver = webdriver.Chrome(options=chrome_options)

# CSV file to save data
csv_file = open('engineering_courses.csv', mode='w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['University', 'Faculty', 'Field', 'Program', 'Intake per Course', 'Intake per TCAS Round', 'Tuition Fee'])

def extract_program_details(url):
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    
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

try:
    driver.get('https://course.mytcas.com/universities/')
    wait = WebDriverWait(driver, 10)

    # Retrieve and iterate over each university
    a_tags = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.brand')))
    university_links = [(a.text, a.get_attribute('href')) for a in a_tags]

    for university_name, link_url in university_links:
        try:
            print(f"Successfully accessed {university_name} at {link_url}")

            # Navigate to the university link
            driver.get(link_url)
            time.sleep(0.25)  # Allow some time for the page to load

            # Retrieve faculty links and filter them
            faculty_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href^="/universities/"][href*="/faculties/"]')))
            faculty_links_filtered = [(fl.get_attribute('innerText').strip(), fl.get_attribute('href')) 
                                      for fl in faculty_links if "คณะวิศวกรรมศาสตร์" in fl.get_attribute('innerText').strip()]

            for faculty_name, faculty_url in faculty_links_filtered:
                try:
                    print(f"Successfully accessed {faculty_name} at {faculty_url}")

                    driver.get(faculty_url)
                    time.sleep(0.25)

                    # Retrieve all field links for the faculty
                    field_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href*="/fields/"]')))
                    field_links = [(field.get_attribute('innerText').strip(), field.get_attribute('href')) for field in field_links]
                    
                    # Loop over each field
                    for field_name, field_url in field_links:
                        try:
                            print(f"Successfully accessed {field_name} at {field_url}")
                            driver.get(field_url)
                            time.sleep(0.25)
                            
                            # Retrieve all program links for the field
                            program_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href*="/programs/"]')))
                            for program_link in program_links:
                                try:
                                    program_name = program_link.text
                                    program_url = program_link.get_attribute('href')
                                    print(f"Successfully accessed {program_name} at {program_url}")
                                    driver.get(program_url)
                                    time.sleep(0.25)
                                    program_details = extract_program_details(program_url)
                                            
                                    
                                    # Collect relevant details
                                    intake_per_course = program_details.get('จำนวนรับ', 'N/A')
                                    intake_per_tcas_round = program_details.get('จำนวนรับแต่ละรอบ', 'N/A')
                                    tuition_fee = program_details.get('ค่าเทอม', 'N/A')

                                    # Write to CSV
                                    csv_writer.writerow([university_name, faculty_name, field_name, program_name, intake_per_course, intake_per_tcas_round, tuition_fee])

                                    driver.back()  # Go back to field page
                                    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href*="/programs/"]')))
                                except StaleElementReferenceException:
                                    print("Stale element reference exception occurred for program link.")
                                    continue

                            driver.back()  # Go back to faculty page
                            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href*="/fields/"]')))

                        except StaleElementReferenceException:
                            print("Stale element reference exception occurred for field link.")
                            continue

                    driver.back()  # Go back to university page
                    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href^="/universities/"][href*="/faculties/"]')))

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
    csv_file.close()
    driver.quit()

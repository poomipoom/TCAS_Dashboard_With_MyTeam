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

def wait_for_elements(driver, by, value, timeout=10):
    try:
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.presence_of_all_elements_located((by, value)))
    except TimeoutException:
        print(f"Timeout occurred while waiting for elements with {by} = {value}")
        return []

def process_program_page(driver, program_url):
    try:
        driver.get(program_url)
        time.sleep(0.25)
        program_details = extract_program_details(program_url)
        if program_details:
            print("Program Details:")
            for key, value in program_details.items():
                print(f"      {key}: {value}")
    except Exception as e:
        print(f"An error occurred while processing program page: {e}")

try:
    driver.get('https://course.mytcas.com/universities/')
    university_links = [(a.text, a.get_attribute('href')) for a in wait_for_elements(driver, By.CSS_SELECTOR, 'a.brand')]

    for university_name, link_url in university_links:
        try:
            print(f"Successfully accessed {university_name} at {link_url}")

            driver.get(link_url)
            faculty_links_filtered = [(fl.get_attribute('innerText').strip(), fl.get_attribute('href')) 
                                      for fl in wait_for_elements(driver, By.CSS_SELECTOR, 'a[href^="/universities/"][href*="/faculties/"]') 
                                      if "คณะวิศวกรรมศาสตร์" in fl.get_attribute('innerText').strip()]

            for faculty_name, faculty_url in faculty_links_filtered:
                try:
                    print(f"Successfully accessed {faculty_name} at {faculty_url}")

                    driver.get(faculty_url)
                    field_links = [(field.get_attribute('innerText').strip(), field.get_attribute('href')) 
                                   for field in wait_for_elements(driver, By.CSS_SELECTOR, 'a[href*="/fields/"]')]

                    for field_name, field_url in field_links:
                        try:
                            print(f"Successfully accessed {field_name} at {field_url}")
                            driver.get(field_url)
                            program_links = [(program.get_attribute('text'),program.get_attribute('href'))
                                for program in wait_for_elements(driver, By.CSS_SELECTOR, 'a[href*="/programs/"]')]
                            
                            for program_name, program_url in program_links:
                                try:
                                    print(f"Successfully accessed {program_name} at {program_url}")
                                    process_program_page(driver, program_url)
                                except StaleElementReferenceException:
                                    print("Stale element reference exception occurred for program link.")
                                    continue

                            driver.back()  # Go back to field page
                            wait_for_elements(driver, By.CSS_SELECTOR, 'a[href*="/programs/"]')

                        except StaleElementReferenceException:
                            print("Stale element reference exception occurred for field link.")
                            continue

                    driver.back()  # Go back to faculty page
                except StaleElementReferenceException:
                    print("Stale element reference exception occurred for faculty link.")
                    continue

            driver.back()  # Go back to university page
        except TimeoutException:
            print(f"Timeout when accessing {university_name} at {link_url}.")
            continue
        except StaleElementReferenceException:
            print("Stale element reference exception occurred for university link.")
            continue

finally:
    driver.quit()

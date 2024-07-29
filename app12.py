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
            for faculty_link in faculty_links:
                try:
                    faculty_name = faculty_link.get_attribute('innerText').strip()
                    if "คณะวิศวกรรมศาสตร์" in faculty_name:
                        faculty_url = faculty_link.get_attribute('href')
                        print(f"Successfully accessed {faculty_name} at {faculty_url}")

                        driver.get(faculty_url)
                        time.sleep(0.25)
                        field_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href*="/fields/"]')))
                        for field_link in field_links:
                            try:
                                field_name = field_link.text
                                field_url = field_link.get_attribute('href')
                                print(f"Successfully accessed {field_name} at {field_url}")
                                driver.get(field_url)
                                time.sleep(0.25)
                                program_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href*="/programs/"]')))
                                for program_link in program_links:
                                    try:
                                        program_name = program_link.text
                                        program_url = program_link.get_attribute('href')
                                        print(f"Successfully accessed {program_name} at {program_url}")
                                        driver.get(program_url)
                                        time.sleep(0.25)
                                        program_details = extract_program_details(program_url)
                                        if program_details:
                                            print("Program Details:")
                                            for key, value in program_details.items():
                                                print(f"      {key}: {value}")
                                                time.sleep(2)
                                        driver.get(faculty_url)
                                        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href*="/fields/"]')))
            # wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.brand')))
                                    except StaleElementReferenceException:
                                        print("Stale element reference exception occurred for program link.")
                                        # continue
                                # driver.get(faculty_url)
                                # wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href*="/fields/"]')))


                            except StaleElementReferenceException:
                                print("Stale element reference exception occurred for field link.")
                                # continue
                        # driver.get(link_url)
                        # wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href^="/universities/"][href*="/faculties/')))


                except StaleElementReferenceException:
                    print("Stale element reference exception occurred for faculty link.")
                    # continue

            # Navigate back to the main page after processing each university
            # driver.get('https://course.mytcas.com/universities/')
            # wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.brand')))

        except TimeoutException:
            print(f"Timeout when accessing {university_name} at {link_url}.")
            continue
        except StaleElementReferenceException:
            print("Stale element reference exception occurred for university link.")
            continue

finally:
    driver.quit()
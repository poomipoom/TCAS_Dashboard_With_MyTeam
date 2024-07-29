from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import StaleElementReferenceException
import time

# Set up the Chrome driver
options = Options()
options.add_argument("--headless")  # Run headless for testing
driver = webdriver.Chrome(options=options)


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



def check_university_links():
    # Open the main page
    driver.get('https://course.mytcas.com/universities/')
    
    # Wait for all the university links to load
    wait = WebDriverWait(driver, 10)

    try:
        a_tags = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.brand')))
        
        for a_tag in a_tags:
            university_name = a_tag.text
            link_url = a_tag.get_attribute('href')

            # Navigate to the university link
            driver.get(link_url)
            
            print(f"Successfully accessed {university_name} at {link_url}")
            
            # Wait for the new page to load
            faculty_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href^="/universities/"][href*="/faculties/"]')))

            print(f"University: {university_name}")

            for faculty_link in faculty_links:
                faculty_name = faculty_link.text
                faculty_url = faculty_link.get_attribute('href')

                # Navigate to the faculty link
                driver.get(faculty_url)
                
                # Wait for the faculty page to load
                while True:
                    try:
                        field_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href*="/fields/"]')))
                        
                        # Print fields with "วิศวกรรม"
                        for field_link in field_links:
                            field_name = field_link.text
                            field_url = field_link.get_attribute('href')
                            if 'วิศวกรรม' in field_name:
                                print(f"  Field: {field_name} - {field_url}")
                        
                                driver.get(field_url)

                                program_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href*="/programs/"]')))

                                for program_link in program_links:
                                    program_url = program_link.get_attribute('href')
                                    print(f"  Program URL: {program_url}")

                                    # Extract program details
                                    program_details = extract_program_details(program_url)
                                    if program_details:
                                        print("    Program Details:")
                                        for key, value in program_details.items():
                                            print(f"      {key}: {value}")
                        break
                    except StaleElementReferenceException:
                        print("Stale element reference caught. Re-locating elements.")

                # Navigate back to the faculty page
                driver.back()
                time.sleep(1)  # Small delay to allow page to load properly

            # Navigate back to the main university page
            driver.back()
            time.sleep(1)  # Small delay to allow page to load properly
            
    finally:
        driver.quit()

def main():
    check_university_links()

if __name__ == "__main__":
    main()


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up the Chrome driver
options = Options()
options.add_argument("--headless")  # Run headless for testing
driver = webdriver.Chrome(options=options)

def check_university_links():
    # Open the main page
    driver.get('https://course.mytcas.com/universities/')
    
    # Wait for all the university links to load
    wait = WebDriverWait(driver, 10)
    
    try:
        while True:
            # Re-fetch university links on each iteration
            a_tags = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.brand')))
            
            for a_tag in a_tags:
                university_name = a_tag.text
                link_url = a_tag.get_attribute('href')

                # Navigate to the university link
                driver.get(link_url)
                
                # Wait for the new page to load
                faculty_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href^="/universities/"][href*="/faculties/"]')))

                print(f"University: {university_name}")

                # Print faculties with "วิศวกรรม"
                for faculty_link in faculty_links:
                    faculty_name = faculty_link.text
                    faculty_url = faculty_link.get_attribute('href')
                    if 'วิศวกรรม' in faculty_name:
                        driver.get(faculty_url)
                        faculty_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href^="/universities/"][href*="/faculties/"]')))

                # Navigate back to the main page
                driver.back()

                # Wait for the main page to reload and break the loop once all universities are processed
                if a_tag == a_tags[-1]:
                    return

    finally:
        driver.quit()

def main():
    check_university_links()

if __name__ == "__main__":
    main()

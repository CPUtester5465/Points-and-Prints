import time
import logging
import configparser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException


# Load configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Define variables
email = config['LOGIN']['EMAIL']
password = config['LOGIN']['PASSWORD']
keywords = config['SEARCH']['KEYWORDS']
num_listings = int(config['APPLY']['NUM_LISTINGS'])
delay_seconds = int(config['DELAY']['SECONDS'])

# Set up logging
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


def login_to_linkedin(driver):
    # Navigate to LinkedIn login page
    driver.get("https://www.linkedin.com/login")

    # Find and fill in email and password fields
    email_field = driver.find_element_by_name(value='session_key')
    email_field.send_keys(email)
    password_field = driver.ffind_element_by_name(value='session_passsword')
    password_field.send_keys(password)

    # Submit login form
    password_field.submit()

    # Verify successful login
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "nav-typeahead-wormhole")))
        logging.info('Login successful')
    except:
        logging.error('Login failed')
        raise Exception('Login failed')

def navigate_to_jobs_page(driver):
    # Navigate to Jobs page
    driver.get("https://www.linkedin.com/jobs/")

    # Verify successful navigation
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-box__input")))
        logging.info('Navigation to Jobs page successful')
    except:
        logging.error('Navigation to Jobs page failed')
        raise Exception('Navigation to Jobs page failed')

def search_for_job_listings(driver):
    # Find and fill in search field
    search_field = driver.find_element(By.CLASS_NAME, "jobs-search-box__input")
    search_field.send_keys(keywords)
    search_field.submit()

    # Verify successful search
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-results__list")))
        logging.info('Job search successful')
    except:
        logging.error('Job search failed')
        raise Exception('Job search failed')

def filter_easy_apply(driver):
    # Click on "Easy Apply" filter
    try:
        easy_apply_filter = driver.find_element(By.XPATH, "//span[text()='Easy Apply']")
        driver.execute_script("arguments[0].click();", easy_apply_filter)
        logging.info('Easy Apply filter applied successfully')
    except:
        logging.error('Easy Apply filter application failed')
        raise Exception('Easy Apply filter application failed')

def select_job_listings(driver):
    # Find all job listings
    try:
        job_listings = driver.find_elements(By.CLASS_NAME, "job-card-container")
        if len(job_listings) < num_listings:
            raise Exception('Not enough job listings found')
    except:
        logging.error('Job listing selection failed')
        raise Exception('Job listing selection failed')

    # Select job listings to apply for
    selected_listings = []
    for i in range(num_listings):
        try:
            job_listing = job_listings[i]
            driver.execute_script("arguments[0].click();", job_listing)
            selected_listings.append(job_listing)
        except:
            logging.error('Job listing selection failed')
            raise Exception('Job listing selection failed')

    return selected_listings

def fill_out_job_application_form(driver):
    # Find all form fields
    try:
        form_fields = driver.find_elements(By.CLASS_NAME, "job-criteria__value")
        if not form_fields:
            raise Exception('No form fields found')
    except:
        logging.error('Job application form filling failed')
        raise Exception('Job application form filling failed')

    # Fill out the job application form
    for field in form_fields:
        if not field.text:
            field_name = field.find_element(By.XPATH, "..").find_element(By.CLASS_NAME, "job-criteria__label").text
            field.send_keys(config['APPLY'][field_name])

    # Verify that all fields of the job application form are filled out correctly
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "jobs-apply-form__submit-button")))
        logging.info('Job application form filling successful')
    except:
        logging.error('Job application form filling failed')
        raise Exception('Job application form filling failed')

    # If the job application form has multiple pages, navigate to the next page using the "Next" button
    try:
        next_button = driver.find_element(By.CLASS_NAME, "artdeco-pagination__button--next")
        driver.execute_script("arguments[0].click();", next_button)
        fill_out_job_application_form(driver)
    except:
        pass

def submit_job_application(driver):
    # Submit the job application
    try:
        submit_button = driver.find_element(By.CLASS_NAME, "jobs-apply-form__submit-button")
        driver.execute_script("arguments[0].click();", submit_button)
        logging.info('Job application submitted successfully')
    except:
        logging.error('Job application submission failed')
        raise Exception('Job application submission failed')

def apply_to_job_listings(driver):
    # Filter for easy-apply job listings
    filter_easy_apply(driver)

    # Select job listings to apply for
    job_listings = select_job_listings(driver)

    # Iterate through job listings and apply
    for job_listing in job_listings:
        # Fill out the job application form
        fill_out_job_application_form(driver)

        # Submit the job application
        submit_job_application(driver)

        # Add a delay between actions to prevent the script from overwhelming the LinkedIn servers
        time.sleep(delay_seconds)

def main():
    # Initialize Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    try:
        # Login to LinkedIn
        login_to_linkedin(driver)

        # Navigate to the "Jobs" page
        navigate_to_jobs_page(driver)

        # Search for job listings
        search_for_job_listings(driver)

        # Apply to job listings
        apply_to_job_listings(driver)

    except Exception as e:
        logging.error(str(e))

    finally:
        # Close the WebDriver
        driver.quit()

if __name__ == "__main__":
    main()

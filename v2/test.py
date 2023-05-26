from selenium import webdriver

# инициализация объекта WebDriver
driver = webdriver.Chrome()

# переход на страницу LinkedIn
driver.get('https://www.linkedin.com')

# вход на LinkedIn
email = 'tderzav@gmail.com'
password = 'sf569j09630'
driver.find_element_by_id('username').send_keys(email)
driver.find_element_by_id('password').send_keys(password)
driver.find_element_by_css_selector('.btn__primary--large').click()

# поиск вакансий
keywords = ['devops', 'devops engineer']
for keyword in keywords:
    search_box = driver.find_element_by_css_selector('.search-global-typeahead__input')
    search_box.send_keys(keyword)
    search_box.submit()

    # подача заявки на вакансию
    num_listings = 1
    for i in range(num_listings):
        job_listing = driver.find_element_by_css_selector('.jobs-search-results__list li')
        job_listing.click()

        # заполнение формы заявки на вакансию
        driver.find_element_by_css_selector('.jobs-apply-button').click()
        driver.find_element_by_css_selector('.jobs-apply-form__resume-upload input[type="file"]').send_keys('/path/to/resume.pdf')
        driver.find_element_by_css_selector('.jobs-apply-form__submit-button').click()

        # задержка между действиями скрипта
        delay_seconds = 10
        time.sleep(delay_seconds)

# закрытие браузера
driver.quit()

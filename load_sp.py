from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# CONFIG FILE
USERNAME = ""
PWD = ""
# Change to relative path
DRIVER_PATH = ""

# Run without GUI
options = Options()
#options.headless = true
options.add_argument("--window-size=1920,1200")

# Navigate to login page
driver = webdriver.Chrome(options = options, executable_path = DRIVER_PATH)
driver.implicitly_wait(0)
driver.get("https://www.spglobal.com/ratings/en/index")
login_button = driver.find_element_by_xpath("//a[@class='header-link login']").click()

# Login
username = driver.find_element_by_xpath("//input[@id='username01']").send_keys(USERNAME)
password = driver.find_element_by_xpath("//input[@id='password01']").send_keys(PWD)
submit = driver.find_element_by_xpath("//button[@type='submit']").click()

# Accept cookies
cookies = driver.find_element_by_xpath("//button[@id='onetrust-accept-btn-handler']").click()

# Allow for popup to disappear
time.sleep(1.5)

companies = ["APPLE", "MICROSOFT", "DUCK CREEK"]

# NEED TO INCLUDE WAITS!
for company in companies:
    time.sleep(2)
    # Go to next company
    next_search = driver.find_element_by_xpath("//button[starts-with(@class, 'button__search')]").click()
    results = driver.find_element_by_xpath("//div[@class='find__input-box']/input").send_keys(company)
    results = driver.find_element_by_xpath("//div[starts-with(@class, 'find__input-box')]/button").click()

    time.sleep(3)
    # Check if there are results - skip to next if not
    if (len(driver.find_elements_by_xpath("//div[@class='row results-header']")) > 0):
        if (len(driver.find_elements_by_xpath("//div[@class='table-module__column']/p/a")) > 0):
            company = driver.find_element_by_xpath("//div[@class='table-module__column']/p/a").click()
        else:
            continue

    # Extract data, store in MongoDB should be done foreach from a list of companies.

# Done scraping data

time.sleep(5)

print("Quitting...")
driver.quit()

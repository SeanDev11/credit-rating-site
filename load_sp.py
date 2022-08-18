from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# Credentials
USERNAME = "sean.devine24@gmail.com"
PWD = "Full$tack2022!"
# Chromedriver must be in PATH
DRIVER_PATH = "/Users/seandevine/Desktop/Life/PersonalProjects/credit-rating-site/chromedriver"

# Run without GUI
options = Options()
#options.headless = True
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
if (len(driver.find_elements_by_xpath("//button[@id='onetrust-accept-btn-handler']")) > 0):
    cookies = driver.find_element_by_xpath("//button[@id='onetrust-accept-btn-handler']").click()

# Allow for popup to disappear
#time.sleep(1.5)

companies = ["APPLE", "MICROSOFT", "DUCK CREEK"]
wait = WebDriverWait(driver, timeout=10, poll_frequency=0.25)

# NEED TO INCLUDE WAITS!
for company in companies:
    print(company)
    # Go to next company
    next_search = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[starts-with(@class, 'button__search')]")))
    next_search.click()
    results = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='find__input-box']/input")))
    results.send_keys(company)
    results = driver.find_element_by_xpath("//div[starts-with(@class, 'find__input-box')]/button").click()

    # Check if there are results - skip to next if not
    try:
        wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='table-module__row']")))
    except TimeoutException:
        print("NOT FOUND")
        continue
    print("dont print after not found")
    if (len(driver.find_elements_by_xpath("//div[@class='row results-header']")) > 0):
        #if (len(driver.find_elements_by_xpath("//div[@class='table-module__column']/p/a")) > 0):
        company = driver.find_element_by_xpath("//div[@class='table-module__column']/p/a").click()

    # NOW ABLE TO - find sub elements. refactor to use By.XXX, wait for proper elements perhaps sub elements

    # Extract data, store in MongoDB should be done foreach from a list of companies.
    # wait.until(EC.visibility_of_element_located((By.ID, "page1")))
    wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='table-module__row']")))
    #ratings = driver.find_elements_by_xpath("//div[@class='table-module__row']")
    ratings = driver.find_element(By.ID, "page1").find_elements(By.CLASS_NAME, "table-module__row")
    print(f"RATING COUNT {len(ratings)}")
    wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "table-module__column")))
    for rating in ratings:
        info = rating.find_elements(By.CLASS_NAME, "table-module__column")
        for i in info:
            print(i.text)

        print("-----------")





        
# Done scraping data

time.sleep(5)

print("Quitting...")
driver.quit()

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
import time
from pymongo import MongoClient
import csv

# TODO refactor into functions
file = open("sp500_constituents.csv")
csvreader = csv.reader(file)
next(csvreader)
companies = []
for row in csvreader:
    companies.append(row)

# Credentials

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

wait = WebDriverWait(driver, timeout=3, poll_frequency=0.25)

allRatings = []

for company in companies:
    ratingsList = []
    company = company[1]
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
        continue
    if (len(driver.find_elements_by_xpath("//div[@class='row results-header']")) > 0):
        company = driver.find_element_by_xpath("//div[@class='table-module__column']/p/a").click()

    # NOW ABLE TO - find sub elements. refactor to use By.XXX, wait for proper elements perhaps sub elements

    wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='table-module__row']")))
    wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "table-module__column")))

    company_name = driver.find_element(By.XPATH, "//div[@class='content']/h1").text
    try:
        ratings = driver.find_element(By.ID, "page1").find_elements(By.CLASS_NAME, "table-module__row")
    except:
        continue

    ratingsCount = len(ratings)
    idx = 0
    while (idx < ratingsCount):
        try:
            info = ratings[idx].find_elements(By.CLASS_NAME, "table-module__column")
            info_dict = {"company": company_name, "ratingType": info[0].text,
                         "rating": info[1].find_element(By.XPATH, "//h5").text,
                         "ratingDate": info[2].text, "lastReviewDate": info[3].text,
                         "regulatoryIdentifiers": info[4].text, "outlook": info[5].text,
                         "outlookDate": info[6].text}
        except StaleElementReferenceException:
            wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='table-module__row']")))
            wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "table-module__column")))
            ratings = driver.find_element(By.ID, "page1").find_elements(By.CLASS_NAME, "table-module__row")
            continue
        
        ratingsList.append(info_dict)
        idx += 1
        
    allRatings.append({company_name: ratingsList})

# Done scraping data
time.sleep(5)

# Insert data into mongoDB
cluster = "mongodb+srv://dbAdmin:dbAdmin@creditrating.nijkfp8.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(cluster)
# client.SPratings is prod db
db = client.CreditRating
ratings = db.ratings
ratings.insert_many(allRatings)



print("Quitting...")
driver.quit()

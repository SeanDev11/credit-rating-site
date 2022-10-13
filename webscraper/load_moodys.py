# load_moodys.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
import time
import csv
from pymongo import MongoClient

# TODO refactor into functions
file = open("sp500_constituents.csv")
csvreader = csv.reader(file)
next(csvreader)
companies = []
for row in csvreader:
    companies.append(row)

print(len(companies))

# Credentials
USERNAME = "sean.devine24@gmail.com"
PWD = "Full$tack2022!"

# Chromedriver must be in PATH
DRIVER_PATH = "/Users/seandevine/Desktop/Life/PersonalProjects/credit-rating-site/chromedriver"

# Run without GUI
options = Options()
#options.headless = True
options.add_argument("--window-size=1920,1200")

# Navigate to home page & accept cookies
driver = webdriver.Chrome(options = options, executable_path = DRIVER_PATH)
driver.implicitly_wait(0)
driver.get("https://www.moodys.com")

if (len(driver.find_elements(By.ID, "onetrust-accept-btn-handler")) > 0):
    driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
    time.sleep(1)

wait = WebDriverWait(driver, timeout=20, poll_frequency=0.25)
wait_med = WebDriverWait(driver, timeout=60, poll_frequency=0.5)
wait_long = WebDriverWait(driver, timeout=180, poll_frequency=0.5)

# Login
loginButton = driver.find_element(By.CSS_SELECTOR, "[data-testid='sign-in']").click()
email = driver.find_element(By.CSS_SELECTOR, "[data-testid='emailInput']").send_keys(USERNAME)
driver.find_element(By.CSS_SELECTOR, "[data-testid='emailContinueButton']").click()
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='password']")))
password = driver.find_element(By.CSS_SELECTOR, "[data-testid='password']").send_keys(PWD)
driver.find_element(By.CSS_SELECTOR, "[data-testid='loadingButton']").click()
time.sleep(10)

allRatings = []
notFound = []
#companies = [["MMM", "3M", "IND"], ["KMX", "CarMax", "CD"], ["CDAY", "Ceridian", "IT"], ["CE", "Celanese", "MAT"], ["ALK", "Alaska Air Group", "MAT"]]
for company in companies[400:505]:
    ratingsList = []
    ticker = company[0]
    name = company[1]
    industry = company[2]
    
    if (company == companies[400]):
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='searchbox-input']")))
        search = driver.find_element(By.CSS_SELECTOR, "[data-testid='searchbox-input']").send_keys(name)
        search = driver.find_element(By.CSS_SELECTOR, "[data-testid='searchbox-input']").send_keys(Keys.ENTER)
    else:
        print(name)
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "search-widget")))
        # Try changing to visibility
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "search-box-inner"))).click()
        time.sleep(2)
        found = False
        while (not(found)):
            try:
                search = driver.find_element(By.XPATH, "//div[@class='search-widget']/div/form/div/input").send_keys(ticker)
                found = True
            except (ElementNotInteractableException, NoSuchElementException) as e:
                time.sleep(5)

        found = False
        while (not(found)):
            try:
                search = driver.find_element(By.XPATH, "//div[@class='search-widget']/div/form/div/input").send_keys(Keys.ENTER)        
                found = True
            except (ElementNotInteractableException, NoSuchElementException) as e:
                time.sleep(5)

    # Distinguish between results page and individual company page
    time.sleep(2)
    wait_long.until(EC.element_to_be_clickable((By.CLASS_NAME, "search-widget")))
    time.sleep(5)
    if (len(driver.find_elements(By.CLASS_NAME, "search-box-input-container")) > 0):
        print("RESULTS PAGE")
        if ((len(driver.find_elements(By.XPATH, "//div[@class='result-type organizations']")) +
            len(driver.find_elements(By.XPATH, "//div[@class='result-type organizations active']"))) == 0):
            print("NO ORGS AS RESULTS")
            notFound.append(company)
            continue

        if (len(driver.find_elements(By.XPATH, "//div[@class='result-type organizations']")) > 0):
            clicked = False
            while (not(clicked)):
                try:
                    driver.find_element(By.XPATH, "//div[@class='result-type organizations']").click()
                    clicked = True
                except (ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException) as e:
                    time.sleep(5)
        else:
            clicked = False
            while (not(clicked)):
                try:
                    driver.find_element(By.XPATH, "//div[@class='result-type organizations active']").click()
                    clicked = True
                except (ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException) as e:
                    time.sleep(5)
                    
        time.sleep(2)
        
        subHeaderIdx = 0
        subHeaders = driver.find_elements(By.CLASS_NAME, "sub-head")
        try:
            subHeadersNum = len(subHeaders)
        except:
            time.sleep(2)
            subHeaders = driver.find_elements(By.CLASS_NAME, "sub-head")
            subHeadersNum = len(subHeaders)
            
        clicked = False
        while (subHeaderIdx < 10 and subHeaderIdx < subHeadersNum):
            try:
                subHeader = subHeaders[subHeaderIdx].text
            except (ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException):
                time.sleep(3)
                subHeaders = driver.find_elements(By.CLASS_NAME, "sub-head")
                continue
            
            print(subHeader)
            if (subHeader.endswith("|" + ticker)):
                print("FOUND TICKER IN SUBHEADER")
                print(subHeaderIdx)
                clicked = False
                while (not(clicked)):
                    try:
                        driver.find_element(By.XPATH, f"//div[@class='result-detail'][{subHeaderIdx+1}]/div/a").click()
                        clicked = True
                    except (ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException, TimeoutException) as e:
                        time.sleep(5)
                        if (type(e) == TimeoutException):
                            driver.get(driver.current_url)
                            time.sleep(10)
                            driver.refresh()
                            clicked = True
                            time.sleep(10)
                            
                subHeaderIdx = 20
            subHeaderIdx += 1
            
        if (not(clicked)):
            # Skip to next company
            notFound.append(company)
            print("Ticker not found in subheader")
            continue
    else:
        print("INDIVIDUAL COMP")
        if ((len(driver.find_elements(By.CLASS_NAME, "orginfo-container")) == 0) or
            not("Ticker" in driver.find_element(By.XPATH, "//div[@class='orginfo-container']/ul/li/div").text) or
            not(ticker in driver.find_element(By.XPATH, "//div[@class='orginfo-container']/ul/li/div[2]").text)):
            print("SKIPPED INDIVIDUAL COMP")
            notFound.append(company)
            continue

    wait_long.until(EC.element_to_be_clickable((By.ID, "ratingAssessments")))
    driver.find_element(By.ID, "ratingAssessments").click()

    company_name = driver.find_element(By.XPATH, "//li[@class='title-analyst']/div").text

    if (driver.find_element(By.ID, "byClass").value_of_css_property("cursor") == "not-allowed"):
        notFound.append(company)
        print("No by class button")
        continue
        
    # Get data
    try:
        wait_med.until(EC.visibility_of_element_located((By.ID, "rating-table")))
    except TimeoutException:
        # No ratings for this entity
        print("No rating table")
        notFound.append(company)
        continue
    ratings = driver.find_element(By.ID, "rating-table").find_elements(By.CSS_SELECTOR, "[data-key]")
    ratingsCount = len(ratings)
    idx = 0

    while (idx < ratingsCount):
        try:
            info = ratings[idx].find_elements(By.CSS_SELECTOR, "[data-index]")
            info_dict = {"entity": company_name, "ratingType": info[0].text,
                         "rating": info[1].text, "date": info[2].text,
                         "action": info[3].text}
        except StaleElementReferenceException:
            wait.until(EC.visibility_of_element_located((By.ID, "rating-table")))
            ratings = driver.find_element(By.ID, "rating-table").find_elements(By.CSS_SELECTOR, "[data-key]")
            continue
        
        ratingsList.append(info_dict)
        idx += 1

    allRatings.append({"company": company_name, "ticker": ticker,
                       "industry": industry, "ratings": ratingsList})
    
# Done scraping data
time.sleep(10)

print(allRatings)
print(len(allRatings))

print(notFound)
print(len(notFound))

fp = open(r"test7.txt", "w")
for rat in allRatings:
    fp.write("%s\n" % rat)
fp.close()

fil = open(r"notfound7.txt", "w")
for c in notFound:
    fil.write("%s\n" % c)
fil.close()

# Insert data into mongoDB
cluster = "mongodb+srv://dbAdmin:dbAdmin%24@creditrating.nijkfp8.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(cluster)
db = client.MY
ratings = db.ratings
ratings.insert_many(allRatings)

print("Quitting...")
driver.quit()


# ALL, MO, ATVI

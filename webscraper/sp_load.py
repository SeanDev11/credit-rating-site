import requests
from bs4 import BeautifulSoup

session = requests.Session()

# Get this from credentials file
payload = {'username' : '*****',
           'password' : '*******'}

page = session.post("https://login.spglobal.com/oam/server/auth_cred_submit", data = payload)

print(page.status_code)
print(page.is_redirect)
print(page.url)

#page = session.get("https://disclosure.spglobal.com/ratings/en/regulatory/search-result/searchType/Entity/searchTerm/Apple")
page = session.get("https://www.spglobal.com/ratings/en/index")
print(page.status_code)
print(page.is_redirect)
print(page.url)


soup = BeautifulSoup(page.content, "html.parser")

print(soup)

results = soup.find(id="consolidatedSearch_content")

#"div", class_ = "table-module__column")

print(results)

#results = results.get("p")
#.get("a").get("href")

#print(results)

# .find_next("a", class_ = "link-black link-black-hover text-underline")






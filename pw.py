from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

p = sync_playwright().start()

browser = p.chromium.launch(headless=False) 
# playwright에 기본으로 headless가 true로 되어있어서 코드가 실행되어도 브라우저가 뜨지 않는다. 
# 그래서 headless를 false로 설정해준다.

page = browser.new_page()

page.goto("https://www.wanted.co.kr/search?query=flutter")

# time.sleep(5)

# page.click("button.Aside_searchButton__Xhqq3")

# time.sleep(5)

# page.get_by_placeholder("검색어를 입력해 주세요.").fill("python")

# time.sleep(5)

# page.keyboard.press("Enter")

# time.sleep(10)

# page.click("a#search_tab_position")

time.sleep(5)

page.keyboard.press("End")

time.sleep(5)

button_element = page.wait_for_selector('[data-testid="SearchContentViewMoreButton"]')
button_element.click()

for x in range(5):
  page.keyboard.press("End")
  time.sleep(5)

content = page.content()

p.stop()

soup = BeautifulSoup(content, "html.parser")

jobs = soup.find_all("div", class_="JobCard_container__FqChn")

jobs_db = []

for job in jobs:
  link = f"https://www.wanted.co.kr{job.find('a')['href']}"
  title = job.find("strong", class_="JobCard_title__ddkwM").text
  company = job.find("span", class_="JobCard_companyName__vZMqJ").text
  reward = job.find("span", class_="JobCard_reward__sdyHn").text
  job = {
    "link": link,
    "title": title,
    "company": company,
    "reward": reward
  }
  jobs_db.append(job)
  
  print(jobs_db)
  
file = open("jobs.csv", "w")
writter = csv.writer(file)
writter.writerow([
  "link",
  "title",
  "company",
  "reward",
])

for job in jobs_db:
  writter.writerow(job.values())
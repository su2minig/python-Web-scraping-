from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup

p = sync_playwright().start()

browser = p.chromium.launch(headless=False) 
# playwright에 기본으로 headless가 true로 되어있어서 코드가 실행되어도 브라우저가 뜨지 않는다. 
# 그래서 headless를 false로 설정해준다.

page = browser.new_page()

page.goto("https://www.wanted.co.kr/")

time.sleep(5)

page.click("button.Aside_searchButton__Xhqq3")

time.sleep(5)

page.get_by_placeholder("검색어를 입력해 주세요.").fill("python")

time.sleep(5)

page.keyboard.press("Enter")

time.sleep(10)

page.click("a#search_tab_position")

time.sleep(5)

for x in range(5):
  page.keyboard.press("End")
  time.sleep(5)

content = print(page.content())

p.stop()

soup = BeautifulSoup(content, "html.parser")
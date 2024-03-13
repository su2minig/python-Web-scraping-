from playwright.sync_api import sync_playwright

p = sync_playwright().start()

browser = p.chromium.launch(headless=False) 
# playwright에 기본으로 headless가 true로 되어있어서 코드가 실행되어도 브라우저가 뜨지 않는다. 
# 그래서 headless를 false로 설정해준다.

page = browser.new_page()

page.goto("https://www.google.com")

page.screenshot()
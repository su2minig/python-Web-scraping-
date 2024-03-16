from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

class JobsScraper:
    def __init__(self):
        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch(headless=False)
        self.page = self.browser.new_page()
        self.jobs_db = []

    def scrape_jobs(self, job):
        self.page.goto(f"https://www.wanted.co.kr/search?query={job}")
        file_name = f"jobs_{job}.csv"

        time.sleep(5)

        self.page.keyboard.press("End")

        time.sleep(5)

        button_element = self.page.wait_for_selector('[data-testid="SearchContentViewMoreButton"]')
        button_element.click()

        for x in range(5):
            self.page.keyboard.press("End")
            time.sleep(5)

        content = self.page.content()

        soup = BeautifulSoup(content, "html.parser")

        jobs = soup.find_all("div", class_="JobCard_container__FqChn")

        for job in jobs:
            link = f"https://www.wanted.co.kr{job.find('a')['href']}"
            title = job.find("strong", class_="JobCard_title__ddkwM").text
            company = job.find("span", class_="JobCard_companyName__vZMqJ").text
            reward = job.find("span", class_="JobCard_reward__sdyHn").text
            job_info = {
                "link": link,
                "title": title,
                "company": company,
                "reward": reward
            }
            self.jobs_db.append(job_info)

        self.file = open(file_name, mode="w", encoding="utf-8", newline="")
        self.writer = csv.writer(self.file)
        self.writer.writerow(["title", "company", "reward", "link"])
        
        for job in self.jobs_db:
          self.writer.writerow(job.values())

    def close(self):
        self.p.stop()

# 검색어 리스트
jobs = ["flutter", "python", "node.js"]

# JobsScraper 객체 생성
scraper = JobsScraper()

# 검색어마다 스크랩 및 저장 수행
for job in jobs:
    scraper.scrape_jobs(job)
    

# Playwright 종료
scraper.close()
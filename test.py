from playwright.sync_api import sync_playwright
import time, requests
from bs4 import BeautifulSoup

class web_scraper:
  def __init__(self):
    self.jobs = []
    self.p = sync_playwright().start()
    self.browser = self.p.chromium.launch(headless=False)
    self.page = self.browser.new_page()
    
  def get_page(self, language):
    print(f"https://web3.career/{language}-jobs")
    self.page.goto(f"https://web3.career/{language}-jobs")
    time.sleep(5)

    while True:
      button_state = self.page.wait_for_selector("li.next")
      if "disabled" in button_state.get_attribute("class"):
        content = self.page.content()
        soup = BeautifulSoup(content, "html.parser")
        
        last_page = int(soup.find("li",class_="active").text)
        break
      else:
        button = self.page.wait_for_selector('a[aria-label="next"]')
        button.click()
        time.sleep(5)
        
    for i in range(1, last_page + 1):
      response = requests.get(f"https://web3.career/{language}-jobs?page={i}")
      soup = BeautifulSoup(response.content, "html.parser")
      
      jobs = soup.find("tbody", class_="tbody").find_all("tr", class_="table_row")
      for job in jobs:
        title = job.find("h2", class_="fs-6 fs-md-5 fw-bold my-primary")
        company = job.find("h3")
        location = job.find_all("td", class_="job-location-mobile")[-1].find_all("a")
        reward = job.find("p", class_="text-salary")
        
        title_text = title.text.strip() if title else None
        company_text = company.text.strip() if company else None
        location_text = ', '.join([x.text.strip() for x in location]) if location else None
        reward_text = reward.text.strip() if reward else None
        
        data = {
          "title": title_text,
          "company": company_text,
          "reward": reward_text,
          "location": location_text,
        }
        self.jobs.append(data)
    
  def get_jobs(self):
    print(self.jobs)
    return self.jobs


scraper = web_scraper()

scraper.get_page("cryptography")

scraper.get_jobs()

scraper.p.stop()
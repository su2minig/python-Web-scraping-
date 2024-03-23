from playwright.sync_api import sync_playwright
import time, requests, re
from flask import Flask, render_template, request, redirect
from bs4 import BeautifulSoup

class web_scraper:

  def __init__(self, language):
    self.web3_jobs = []
    self.berlin_jobs = []
    self.wework_jobs = []
    self.language = language
    self.p = sync_playwright().start()
    self.browser = self.p.chromium.launch(headless=False)
    self.page = self.browser.new_page()
    self.get_page()
  
  def get_page(self):
    # web3.career
    self.page.goto(f"https://web3.career/{self.language}-jobs")
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
      response = requests.get(f"https://web3.career/{self.language}-jobs?page={i}")
      soup = BeautifulSoup(response.content, "html.parser")
      
      # jobs = [job for job in soup.find("tbody", class_="tbody").find_all("tr", class_="table_row") if not job.get('id') or not re.match(r'sponsor_\d+', job.get('id'))]
      all = soup.find("tbody", class_="tbody").find_all("tr", class_="table_row")
      jobs = []
      
      for job in all:
        job_id = job.get("id")
        
        if job_id is None or not re.match(r'sponsor_\d+', job_id):
          jobs.append(job)
      
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
        self.web3_jobs.append(data)
    
    # berlinstartupjobs
    response = requests.get(
      f"https://berlinstartupjobs.com/skill-areas/{self.language}",
      headers={
          "User-Agent":
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
      })

    soup = BeautifulSoup(response.content, "html.parser")

    berlinstartupjobs_jobs = soup.find("ul", class_="jobs-list-items").find_all("li")

    for job in berlinstartupjobs_jobs:
      title = job.find("h4", class_="bjs-jlid__h").text
      company = job.find("a", class_="bjs-jlid__b").text
      info = job.find("div", class_="bjs-jlid__description").text
      link = job.find("a")["href"]
      data = {
        "title": title,
        "company": company,
        "info": info,
        "link": link
        }
      self.berlin_jobs.append(data)
    # weworkremotely
    self.page.goto(f"https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term={self.language}")

    time.sleep(5)
    button = self.page.wait_for_selector('a[href="/categories/remote-full-stack-programming-jobs"]')
    button.click()
    
    time.sleep(5)
    
    url = self.page.url
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content, "html.parser")

    weworkremotely_jobs = soup.find("section", class_="jobs").find_all("li")[1:-1]

    for job in weworkremotely_jobs:
      title = job.find("span", class_="title").text
      company, position, location = job.find_all("span", class_="company")
      url = job.find("div", class_="tooltip--flag-logo").next_sibling["href"]
      job_data = {
          "title": title,
          "company": company.text,
          "position": position.text,
          "location": location.text,
          "url": f"https://weworkremotely.com{url}",
      }
      self.wework_jobs.append(job_data)
    
    self.page.go_back()
    
    button = self.page.wait_for_selector('a[href="/categories/remote-back-end-programming-jobs"]')
    button.click()
    time.sleep(5)
    
    url = self.page.url
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content, "html.parser")

    weworkremotely_jobs = soup.find("section", class_="jobs").find_all("li")[1:-1]

    for job in weworkremotely_jobs:
      title = job.find("span", class_="title").text
      company, position, location = job.find_all("span", class_="company")
      url = job.find("div", class_="tooltip--flag-logo").next_sibling["href"]
      job_data = {
          "title": title,
          "company": company.text,
          "position": position.text,
          "location": location.text,
          "url": f"https://weworkremotely.com{url}",
      }
      self.wework_jobs.append(job_data)
      
  def get_web3(self):
    return self.web3_jobs
  
  def get_berlin(self):
    return self.berlin_jobs
  
  def get_wework(self):
    return self.wework_jobs



app = Flask("JobScrapper")

db = {}

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/search")
def search():
  keyword = request.args.get("keyword")
  if keyword == None:
    return render_template("home.html")
  if keyword in db:
    web3_jobs = db[keyword]["web3"]
    berlin_jobs = db[keyword]["berlin"]
    wework_jobs = db[keyword]["wework"]
  else:
    scraper = web_scraper(keyword)
    web3_jobs = scraper.get_web3()
    berlin_jobs = scraper.get_berlin()
    wework_jobs = scraper.get_wework()
    db[keyword] = {
      "web3": web3_jobs,
      "berlin": berlin_jobs,
      "wework": wework_jobs
    }
  
  result = {
    "web3": web3_jobs,
    "berlin": berlin_jobs,
    "wework": wework_jobs
  }
  print("wework",wework_jobs)
  return render_template("search.html", keyword=keyword, result=result)

app.run('0.0.0.0',port=5000,debug=True)
from bs4 import BeautifulSoup
import requests

from flask import Flask, render_template, request

class web_scraper:

  def __init__(self, language):
    self.url = f"https://remoteok.com/remote-{language}-jobs"
    self.jobs = []
    self.language = language
    self.get_page()
    self.get_jobs()

  def get_page(self):
    response = requests.get(self.url, headers={
      "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
                            })
    soup = BeautifulSoup(response.content, "html.parser")

    jobs = soup.find("div",class_="container").find_all("tr", class_="job")
    for job in jobs:
      title = job.find("h2", itemprop="title").text
      company = job.find("h3", itemprop="name").text
      url = job.find("a", class_="preventLink")["href"]
      location = job.find("div", class_="location").text
      
      self.jobs.append({
        "title": title.strip(),
        "company": company.strip(),
        "url": f"https://remoteok.com{url}",
        "location": location,
      })
      
  def get_jobs(self):
    print(self.jobs)
    return self.jobs

app = Flask("JobScrapper")

@app.route("/")
def home():
  return render_template("home.html", name="sumin")


@app.route("/search")
def hello():
  keyword = request.args.get("keyword")
  jlist = web_scraper(keyword)
  jobs = jlist.get_jobs()
  print("________________________________")
  print(jobs)
  print("________________________________")
  result = {
      "jobs": jobs,
      "keyword": keyword
  }
  return render_template("search.html", result=result)


app.run('0.0.0.0',port=5000,debug=True)
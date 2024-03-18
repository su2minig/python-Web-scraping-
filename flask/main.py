from bs4 import BeautifulSoup
import requests
from file import save_to_file

from flask import Flask, render_template, request, redirect, send_file

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

db = {}

@app.route("/")
def home():
  return render_template("home.html", name="sumin")


@app.route("/search")
def search():
  keyword = request.args.get("keyword")
  if keyword == None:
    return render_template("home.html", name="sumin")
  if keyword in db:
    jobs = db[keyword]
  else:
    jlist = web_scraper(keyword)
    jobs = jlist.get_jobs()
    db[keyword] = jobs
    
  result = {
      "jobs": jobs,
      "keyword": keyword
  }
  return render_template("search.html", result=result)

@app.route("/export")
def export():
  keyword = request.args.get("keyword")
  if keyword == None:
    return redirect("/")
  if keyword not in db:
    return redirect(f"/search?keyword={keyword}")
  save_to_file(keyword, db[keyword])
  return send_file(f"{keyword}.csv", as_attachment=True)

app.run('0.0.0.0',port=5000,debug=True)
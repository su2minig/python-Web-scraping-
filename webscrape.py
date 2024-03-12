import requests
from bs4 import BeautifulSoup

languages = ["flutter", "python", "golang"]

class web_scraper:

  def __init__(self, language):
    self.url = f"https://remoteok.com/remote-{language}-jobs"
    self.jobs = []
    self.language = language
    self.get_page()
    print("---------start---------")
    print(self.jobs)
    print("---------finish----------")

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
  
for language in languages:
  scrape = web_scraper(language)
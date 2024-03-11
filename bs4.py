import requests
from bs4 import BeautifulSoup

url = "https://weworkremotely.com/remote-full-stack-programming-jobs"

response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

jobs = soup.find("section", class_="jobs").find_all("li")[1:-1]

for job in jobs:
  title = job.find("span", class_="title").text
  region = job.find("span", class_="region").text
  company, position, _ = job.find_all("span", class_="company")
  conpany = company.text
  position = position.text
  print(f"Title: {title}", f"Region: {region}", f"Company: {company}", f"Position: {position}", sep="\n")
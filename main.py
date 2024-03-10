from requests import get

websites=[
"google.com",
"https://httpstat.us/502",
"https://httpstat.us/404",
"https://httpstat.us/300",
"https://httpstat.us/200",
"https://httpstat.us/101"
]
#https://httpstat.us/xxx 는 http코드를 생성해주는 사이트입니다

results={}

for website in websites:
  if not website.startswith("https://"):
    website = f"https://{website}"
  code = get(website).status_code
  if code >= 500:
    results[website] = "5xx / server error"
  elif code >= 400:
    results[website] = "4xx / client error"
  elif code >= 300:
    results[website] = "3xx / redirection "
  elif code >= 200:
    results[website] = "2xx / successful"
  elif code >= 100:
    results[website] = "1xx / informational response"

print(results)
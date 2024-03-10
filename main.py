from requests import get

websites = (
  "google.com",
  "airbnb.com",
  "twitter.com",
  "facebook.com",
)

for website in websites:
  if not website.startswith("https://"):
    website = f"https://{website}"
    response = get(website)
  print(response) # 200, 429, 400, 200
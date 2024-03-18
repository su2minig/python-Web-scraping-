def save_to_file(filename, jobs):
  file = open(f"{filename}.csv", "w", encoding="utf-8")
  file.write("location, company, title, url\n")
  
  for job in jobs:
    file.write(f"{job['location']},{job['company']},{job['title']},{job['url']}\n")
    
  file.close()
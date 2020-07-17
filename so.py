import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = "https://stackoverflow.com/jobs?q=python"

def extract_page_nb():
  request = requests.get(URL)
  soup = BeautifulSoup(request.text, "html.parser")
  pages = soup.find("div", {"class":"s-pagination"}).find_all('a')
  max_pn = pages[-2].get_text(strip=True)
  return int(max_pn)

def extract_job(html):
  title = html.find("h2").text.strip()
  company, location = html.find("h3").find_all('span', recursive=False)
  company = company.get_text(strip=True)
  location = location.get_text(strip=True)
  job_id = html["data-jobid"]
  return {"title":title, "company":company, "location":location, "link":f"https://stackoverflow.com/jobs/{job_id}"}
  

def request_page(max_pn):
  jobs = []
  for page in range(max_pn):
    print(f"Scrapping SO page {page}")
    request = requests.get(f"{URL}&pg={page+1}")
    soup = BeautifulSoup(request.text, "html.parser")
    results = soup.find_all("div", {"class":"-job"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs

def get_jobs():
  max_pn = extract_page_nb()
  jobs = request_page(max_pn)
  return []
import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"


def extract_page_nb():
  result = requests.get("https://www.indeed.com/jobs?q=python&limit=50")
  soup = BeautifulSoup(result.text, "html.parser")
  pagination = soup.find("div", {"class": "pagination"})
  pages = pagination.find_all('a')
  pgs = []
  for page in pages[:-1]:
      pgs.append(int(page.string))
  #same as pgs.append(int(page.find('span).string)) 그 안에 str 하나 밖에 없어서
  #pg = pg[:-1] same as pg = pg[0:-1]
  max_pn = pgs[-1]
  return max_pn


def extract_job(html):
  title = html.find("h2", {"class": "title"}).find("a")["title"]
  company = html.find("span", {"class": "company"})
  company_anchor = company.find('a')
  if company_anchor is not None:
      company = company_anchor.string.strip()
  else:
      company = company.string.strip()
  location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
  job_id = html["data-jk"]
  return ({
      "title": title,
      "company": company,
      "location": location,
      "link": f"https://www.indeed.com/viewjob?jk={job_id}"
  })


def request_page(max_pn):
  jobs = []
  for page in range(max_pn):
    print(f"Scrapping Indeed page {page}")
    request = requests.get(f"{URL}&start={0*50}")
    soup = BeautifulSoup(request.text, "html.parser")
    job_info = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
    for info in job_info:
        job = extract_job(info)
        jobs.append(job)
  return jobs


def get_jobs():
  max_pn = extract_page_nb()
  jobs = request_page(max_pn)
  return jobs
from selenium import webdriver
from bs4 import BeautifulSoup
from extractors.wwr import extract_wwr_jobs

browser = webdriver.Chrome()

base_url = "https://kr.indeed.com/jobs?q="
search_term = "python"
browser.get(f"{base_url}{search_term}")

results = []
soup = BeautifulSoup(browser.page_source, "html.parser")
job_list = soup.find("ul", class_="css-zu9cdh eu4oa1w0")
jobs = job_list.find_all("li", recursive=False)
for job in jobs:
    zone = job.find("div", class_="mosaic-zone")
    if zone == None:
        anchor = job.select_one("h2 a")
        title = anchor["aria-label"]
        link = anchor["href"]
        company = job.find("span", class_="css-1x7z1ps eu4oa1w0")
        location = job.find("div", class_="css-t4u72d eu4oa1w0")
        job_data = {
            "link": f"https://kr.indeed.com{link}",
            "company": company.string,
            "location": location.string,
            "position": title,
        }
        results.append(job_data)
for result in results:
    print(result)
    print("---------------------")

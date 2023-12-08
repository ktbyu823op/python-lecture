from selenium import webdriver
from bs4 import BeautifulSoup

def get_page_count(keyword):
    browser = webdriver.Chrome()
    base_url = "https://kr.indeed.com/jobs?q="
    browser.get(f"{base_url}{keyword}")

    soup = BeautifulSoup(browser.page_source, "html.parser")
    pagination=soup.find("ul",class_="css-1g90gv6 eu4oa1w0")
   
    pages=pagination.find_all("li",recursive=False)
    count = len(pages)
    if count==0:
        return 1
    elif count>5:
        return 5
    else:
        return count-1
    
def extract_indeed_jobs(keyword):
    pages=get_page_count(keyword)
    print("Found",pages,"pages")
    results = []
    for page in range(pages):
        browser = webdriver.Chrome()

        base_url = "https://kr.indeed.com/jobs"
        final_url=f"{base_url}?q={keyword}&start={page*10}"
        print("Requesting",final_url)
        browser.get(final_url)

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
                    "company": company.string.replace(","," "),
                    "location": location.string.replace(","," "),
                    "position": title.replace(","," ").replace("의 전체 세부 정보",""),
                }
                results.append(job_data)
    return results
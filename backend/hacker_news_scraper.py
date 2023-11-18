import json
from requests_html import HTMLSession
from bs4 import BeautifulSoup


session = HTMLSession()

# Fetch data from a URL and return it as a JSON object
def fetch_json_data(url):
    response = session.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data
    else:
        return None

def scrape_web(url):
    contents = session.get(url)
    soup = BeautifulSoup(contents.text, "html.parser")
    return soup.find("body").text

def get_jobs():
    jobs_url = "https://hacker-news.firebaseio.com/v0/jobstories.json?print=pretty"
    item_url = "https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty"

    session = HTMLSession()
    jobs = fetch_json_data(jobs_url)
    for job in jobs:
        item = fetch_json_data(item_url.format(job))
        if "text" in item.keys():
            yield item["text"]
        elif "url" in item.keys():
            yield scrape_web(item["url"])

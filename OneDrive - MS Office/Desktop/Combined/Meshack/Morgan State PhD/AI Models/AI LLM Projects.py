import requests
from bs4 import BeautifulSoup

urls = [
    "https://meshackkinyua.com/profile1",
    "https://www.afriorbit.space//johndoemeshack"
]

for url in urls:
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        print(f"Scraped {url}: {soup.title.string if soup.title else 'No Title'}")
    else:
        print(f"Failed to fetch {url}")

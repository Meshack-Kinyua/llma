import requests
from bs4 import BeautifulSoup

urls = [
    "https://meshackkinyua.com/",
    "https://www.linkedin.com/in/meshack-ndiritu/"
]

for url in urls:
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        print(f"Scraped {url}: {soup.title.string if soup.title else 'No Title'}")
    else:
        print(f"Failed to fetch {url}")

from bs4 import BeautifulSoup
import requests

url = "https://meshackkinyua.com/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

links = [a['href'] for a in soup.find_all('a', href=True)]
print(links)

def extract_experience(soup):
    # Example: Find all job titles in <h2> tags
    jobs = [h2.get_text(strip=True) for h2 in soup.find_all('h2')]
    return jobs

# Usage
soup = BeautifulSoup(response.content, "html.parser")
experience = extract_experience(soup)
print("Experience:", experience)


import openai

# Example structured data
profile_data = {
    "name": "Meshack Ndiritu",
    "experience": ["Software Engineer at X", "Data Analyst at Y"],
    "education": ["BSc in Computer Science, Z University"]
}

prompt = f"""
Create a professional resume for the following person:
Name: {profile_data['name']}
Experience: {', '.join(profile_data['experience'])}
Education: {', '.join(profile_data['education'])}
"""

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)
print(response['choices'][0]['message']['content'])

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://www.tudoms.org/"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/140.0.0.0 Safari/537.36"
    )
}

response = requests.get(url, headers=headers, timeout=10)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

for link in soup.find_all("a", href=True):
    text = link.get_text(" ", strip=True)

    if (
        "result published" in text.lower()
        and "bim" in text.lower()
        and "6th semester" in text.lower()
    ):
        href = urljoin(url, link["href"])

        print("Title:", text)
        print("Link:", href)

print("Scraping completed!")

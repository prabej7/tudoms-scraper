import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://www.tudoms.org/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/140.0.0.0 Safari/537.36"
    )
}


def scrape_result():
    response = requests.get(
        URL,
        headers=HEADERS,
        timeout=10
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for link in soup.find_all("a", href=True):
        text = link.get_text(" ", strip=True)

        if (
            "result published" in text.lower()
            and "bim" in text.lower()
            # and "6th semester" in text.lower()
        ):
            href = urljoin(URL, link["href"])

            return {
                "title": text,
                "link": href
            }

    return None


result = scrape_result()

if result:
    print("Result found!")
    print("Title:", result["title"])
    print("Link:", result["link"])
else:
    print("No matching result found.")

print("Scraping completed!")
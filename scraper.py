import os
import smtplib
from email.message import EmailMessage
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv


load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")

URL = "https://www.tudoms.org/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/140.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
    "Connection": "keep-alive",
}


def scrape_result():
    session = requests.Session()
    session.headers.update(HEADERS)

    response = session.get(URL, timeout=20)

    print("Status:", response.status_code)

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for link in soup.find_all("a", href=True):
        text = link.get_text(" ", strip=True)

        if (
            "result published" in text.lower()
            and "bim" in text.lower()
            and "6th" in text.lower()
        ):
            href = urljoin(URL, link["href"])

            return {
                "title": text,
                "link": href,
            }

    return None


def send_email(result):
    message = EmailMessage()

    message["Subject"] = result["title"]
    message["From"] = EMAIL_USER
    message["To"] = EMAIL_TO

    message.set_content(
        f"""A new result has been published.

{result["title"]}

View Result:
{result["link"]}
"""
    )

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_USER, EMAIL_PASSWORD)
        smtp.send_message(message)

    print("Email sent successfully!")


def main():
    try:
        result = scrape_result()

        if result:
            print("Result found!")
            print("Title:", result["title"])
            print("Link:", result["link"])

            send_email(result)
        else:
            print("No matching result found.")

        print("Scraping completed!")

    except requests.exceptions.RequestException as error:
        print("Request failed:", error)

    except smtplib.SMTPException as error:
        print("Email failed:", error)

    except Exception as error:
        print("Unexpected error:", error)


if __name__ == "__main__":
    main()
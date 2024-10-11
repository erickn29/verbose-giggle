import requests

from bs4 import BeautifulSoup


def parse_page(page):
    data = requests.get(page)
    soup = BeautifulSoup(data.content, "html.parser")
    tags = soup.find_all("p")
    print(tags)
    for tag in tags:
        print(tag.text)
        if tag.text.startswith("Q"):
            with open("python_questions.txt", "a", encoding="utf-8") as f:
                f.write(f"{tag.text}\n")


if __name__ == "__main__":
    parse_page(
        "https://data-flair.training/blogs/top-python-interview-questions-answer/"
    )

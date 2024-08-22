from bs4 import BeautifulSoup
from .scraper import Scraper


class NovelFullCrawler(Scraper):
    def __init__(self, novel_name):
        self.source_url = "https://novelfull.com"
        self.novel_name = novel_name
        self.records_per_page = 50

    def get_chapter_url(self, chapter: int):
        """Return novel chapter url."""
        page = int((chapter - 1) / self.records_per_page) + 1
        urls = self._get_chapter_urls_from_page(
            f"{self.source_url}/{self.novel_name}.html?page={page}"
        )
        for url in urls:
            chapter_name = url.split("/")[-1]
            chapter_number = int(chapter_name.split("-")[1].replace(".html", ""))
            if chapter_number == chapter:
                return url
        raise ValueError(f"Chapter not found: {chapter}")

    def download_chapter(self, chapter_url):
        response = self.get_response(chapter_url)
        chapter_html = response.text

        return chapter_html

    def _get_chapter_urls_from_page(self, url_page):
        response = self.get_response(url_page)
        soup_chapter_list = BeautifulSoup(response.text, features="html.parser")
        chapters_list = soup_chapter_list.find_all("ul", class_="list-chapter")
        urls = [
            f"{self.source_url}{a['href']}"
            for chapters in chapters_list
            for a in chapters.find_all("a", href=True)
        ]

        return urls

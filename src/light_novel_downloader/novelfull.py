from bs4 import BeautifulSoup
from .scraper import Scraper


class NovelFullCrawler(Scraper):
    def __init__(self, novel_name):
        self.source_url = "https://novelfull.com"
        self.novel_name = novel_name
        self.records_per_page = 50

    def yield_chapter_urls(self, start: int, end: int):
        """Generate novel chapter numbers and corresponding urls.

        start   -- start chapter.
        end     -- end chapter.
        """
        page_start = int((start - 1) / self.records_per_page) + 1
        page_end = int((end - 1) / self.records_per_page) + 1
        for x in range(page_start, page_end + 1):
            urls = self._get_chapter_urls_from_page(
                f"{self.source_url}/{self.novel_name}.html?page={x}"
            )
            for url in urls:
                chapter_name = url.split("/")[-1]
                chapter_number = int(chapter_name.split("-")[1].replace(".html", ""))
                if chapter_number < start:
                    continue
                # assume that the urls are ordered
                if chapter_number > end:
                    break
                yield (chapter_number, url)

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

    def parse_chapter(page_text):
        soup = BeautifulSoup(page_text)
        # update prev and next page buttons
        for a in soup.find_all(["#next_chap", "#prev_chap"], href=True):
            a["href"] = a["href"].split("/")[-1] + ".html"
        chapter_content = soup.select_one("#chapter-content")
        for div in chapter_content.find_all(["iframe", "div"]):
            div.decompose()
        chapter_title = soup.find("span", {"class": "chapter-text"}).contents
        chapter = {
            "webpage": soup,
            "contents": chapter_content,
            "title": chapter_title[0],
        }

        return chapter

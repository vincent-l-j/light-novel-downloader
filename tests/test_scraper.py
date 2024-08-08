import unittest
from unittest.mock import patch
import requests
from src.light_novel_downloader.scraper import Scraper
from src.light_novel_downloader import main


class TestScraper(unittest.TestCase):

    @patch("src.light_novel_downloader.scraper.requests.get")
    def test_get_response_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "<html>Chapter 1 content</html>"

        scraper = Scraper()
        response = scraper.get_response("https://example.com/chapter1")

        self.assertIsNotNone(response.text)
        self.assertIn("Chapter 1 content", response.text)

    @patch("src.light_novel_downloader.scraper.requests.get")
    def test_get_response_failure(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        scraper = Scraper()
        response = scraper.get_response("https://example.com/chapter1")

        self.assertIsNone(response)

    def test_main(self):
        exit_status = main()
        self.assertIsNone(exit_status)


if __name__ == "__main__":
    unittest.main()

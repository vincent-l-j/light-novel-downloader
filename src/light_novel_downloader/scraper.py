import requests


class Scraper:
    def get_response(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {url}: {e}")
            return None

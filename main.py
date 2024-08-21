from src.light_novel_downloader.scraper import Scraper
from pathlib import Path

source = "https://novelfull.com"
path = "/reincarnation-of-the-strongest-sword-god/chapter-1-starting-over.html"
dir_downloads = "downloads"
scraper = Scraper()
r = scraper.get_response(source + path)
page_name = f"{dir_downloads}{path}"
dir_novel = "/".join(page_name.split("/")[:-1])
Path(dir_novel).mkdir(parents=True, exist_ok=True)
with open(page_name, "w") as f_out:
    f_out.write(r.text)

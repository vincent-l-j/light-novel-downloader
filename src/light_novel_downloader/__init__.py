import sys


def main():
    from .scraper import Scraper

    source = "https://novelfull.com"
    path = "/reincarnation-of-the-strongest-sword-god/chapter-1-starting-over.html"
    dir_downloads = "downloads"
    scraper = Scraper()
    r = scraper.get_response(source + path)
    page_name = f"{dir_downloads}{path}"
    with open(page_name, "w") as f_out:
        f_out.write(r.text)


if __name__ == "__main__":
    exit_status = 1
    try:
        main()
        exit_status = 0
    except Exception as e:
        print("Error:", e, file=sys.stderr)
    sys.exit(exit_status)

import requests

source = "https://novelfull.com"
path = "/reincarnation-of-the-strongest-sword-god/chapter-1-starting-over.html"
dir_downloads = "downloads"
r = requests.get(source + path)
page_name = f"{dir_downloads}{path}"
with open(page_name, "w") as f_out:
    f_out.write(r.text)

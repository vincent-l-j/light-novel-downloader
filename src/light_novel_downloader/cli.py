import click
from .novelfull import NovelFullCrawler
from pathlib import Path

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option()
def cli():
    "A command line utility to download light novels."


@cli.command(name="download")
@click.argument("novel_name", type=click.STRING)
@click.option("--start", type=click.INT, default=1, help="starting chapter to download")
@click.option("--end", type=click.INT, default=1, help="ending chapter to download")
def download_page(novel_name: str, start: int, end: int):
    """
    Download a range of chapters from a light novel.

    Args:
        novel_name (str): The name of the novel to download, in hyphenated form.
                          For example: 'reincarnation-of-the-strongest-sword-god'.
        start (int): The starting chapter number to download. Defaults to 1.
        end (int): The ending chapter number to download. Defaults to 1.

    This command will download the specified range of chapters from the given novel.
    Each chapter will be saved as an HTML file in the 'downloads/<novel_name>' directory.
    The chapters will be sequentially downloaded from 'start' to 'end', inclusive.
    Ensure the novel name is properly hyphenated (lowercase words separated by hyphens)
    to match the URL formatting on the source site.

    Example usage:
        `download reincarnation-of-the-strongest-sword-god --start 10 --end 20`

    This will download chapters 10 through 20 of 'Reincarnation of the Strongest Sword God'
    and save them as:
        'downloads/reincarnation-of-the-strongest-sword-god/chapter-0010.html'
        'downloads/reincarnation-of-the-strongest-sword-god/chapter-0011.html'
        ...
        'downloads/reincarnation-of-the-strongest-sword-god/chapter-0020.html'
    """
    dir_novel_downloads = f"downloads/{novel_name.lower()}"
    Path(dir_novel_downloads).mkdir(parents=True, exist_ok=True)
    crawler = NovelFullCrawler(novel_name)
    for chapter_number, chapter_url in crawler.yield_chapter_urls(start, end):
        download_filepath = f"{dir_novel_downloads}/chapter-{chapter_number:04d}.html"
        chapter_html = crawler.download_chapter(chapter_url)
        with open(download_filepath, "w") as f:
            f.write(chapter_html)
        click.echo(f"Downloaded chapter to {download_filepath}")

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
@click.option("--chapter", type=click.INT, default=1, help="chapter to download")
def download_page(novel_name: str, chapter: int):
    """
    Download a specific chapter of a light novel.

    Args:
        novel_name (str): The name of the novel to download, in hyphenated form.
                          For example: 'reincarnation-of-the-strongest-sword-god'.
        chapter (int): The chapter number to download. Defaults to 1 if not provided.

    This command will download the specified chapter from the given novel's page and
    save it as an HTML file in the 'downloads/<novel_name>' directory.
    Ensure the novel name is properly hyphenated (lowercase words separated by hyphens)
    to match the URL formatting on the source site.

    Example usage:
        `download reincarnation-of-the-strongest-sword-god --chapter 10`

    This will download chapter 10 of 'Reincarnation of the Strongest Sword God' to:
        'downloads/reincarnation-of-the-strongest-sword-god/chapter-0010.html'
    """
    dir_novel_downloads = f"downloads/{novel_name.lower()}"
    Path(dir_novel_downloads).mkdir(parents=True, exist_ok=True)
    crawler = NovelFullCrawler(novel_name)
    chapter_url = crawler.get_chapter_url(chapter)
    download_filepath = f"{dir_novel_downloads}/chapter-{chapter:04d}.html"
    chapter_html = crawler.download_chapter(chapter_url)
    with open(download_filepath, "w") as f:
        f.write(chapter_html)
    click.echo(f"Downloaded chapter to {download_filepath}")

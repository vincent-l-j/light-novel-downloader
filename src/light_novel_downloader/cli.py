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
    """Download chapter from NOVEL.

    NOVEL is the name of the novel to be downloaded. Ensure it is hyphenated. e.g. reincarnation-of-the-strongest-sword-god
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

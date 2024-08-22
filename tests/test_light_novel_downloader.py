from unittest.mock import mock_open, patch
from click.testing import CliRunner
from light_novel_downloader.cli import cli


def test_version():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert result.output.startswith("cli, version ")


def test_help():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert result.output.startswith("Usage: ")
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["-h"])
        assert result.exit_code == 0
        assert result.output.startswith("Usage: ")


@patch("light_novel_downloader.cli.NovelFullCrawler")
@patch("light_novel_downloader.cli.Path.mkdir")
@patch("builtins.open", new_callable=mock_open)
def test_download_single_chapter(mock_open_func, mock_mkdir, mock_crawler):
    runner = CliRunner()

    # Define variables for the test
    source = "https://novelfull.com"
    chapter_name = "chapter-1-starting-over.html"
    novel_name = "reincarnation-of-the-strongest-sword-god"
    dir_novel_downloads = f"downloads/{novel_name.lower()}"
    chapter_number = 1
    chapter_url = f"{source}/{novel_name}/{chapter_name}"
    chapter_content = f"<html>Chapter {chapter_number} content</html>"
    download_filepath = f"{dir_novel_downloads}/chapter-{chapter_number:04d}.html"

    # Arrange mocks
    mock_crawler_instance = mock_crawler.return_value
    mock_crawler_instance.get_chapter_url.return_value = chapter_url
    mock_crawler_instance.download_chapter.return_value = chapter_content

    # Act
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            [
                "download",
                novel_name,
                "--chapter",
                str(chapter_number),
            ],
        )

    # Assert
    assert result.exit_code == 0
    assert f"Downloaded chapter to {download_filepath}" in result.output

    # Check that the crawler was instantiated and called with the correct url
    mock_crawler.assert_called_once_with(novel_name)
    mock_crawler_instance.get_chapter_url.assert_called_once_with(chapter_number)
    mock_crawler_instance.download_chapter.assert_called_once_with(chapter_url)

    # Ensure the directory was created
    mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

    # Check that the file was opened for writing and content was written
    mock_open_func.assert_called_once_with(download_filepath, "w")
    mock_open_func().write.assert_called_once_with(chapter_content)

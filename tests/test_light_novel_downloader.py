from unittest.mock import MagicMock, mock_open, patch
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


@patch("light_novel_downloader.cli.Scraper")
@patch("light_novel_downloader.cli.Path.mkdir")
@patch("builtins.open", new_callable=mock_open)
def test_download_single_chapter(mock_open_func, mock_mkdir, mock_scraper):
    runner = CliRunner()

    # Define variables for the test
    source = "https://novelfull.com"
    chapter_name = "chapter-1-starting-over.html"
    novel_name = "reincarnation-of-the-strongest-sword-god"
    chapter_number = 1
    chapter_url = f"{source}/{novel_name}/{chapter_name}"
    chapter_content = f"<html>Chapter {chapter_number} content</html>"
    download_filepath = f"downloads/{novel_name}/{chapter_name}"

    # Arrange mocks
    mock_scraper_instance = mock_scraper.return_value
    mock_response = MagicMock()
    mock_response.text = chapter_content
    mock_scraper_instance.get_response.return_value = mock_response

    # Act
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            [
                "download",
            ],
        )

    # Assert
    assert result.exit_code == 0
    assert f"Downloaded chapter to {download_filepath}" in result.output

    # Check that the scraper was instantiated and called with the correct url
    mock_scraper.assert_called_once_with()
    mock_scraper_instance.get_response.assert_called_once_with(chapter_url)

    # Ensure the directory was created
    mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

    # Check that the file was opened for writing and content was written
    mock_open_func.assert_called_once_with(download_filepath, "w")
    mock_open_func().write.assert_called_once_with(chapter_content)

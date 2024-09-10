from unittest.mock import call, mock_open, patch
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
def test_download_multiple_chapters(mock_open_func, mock_mkdir, mock_crawler):
    runner = CliRunner()

    # Define variables for the test
    source = "https://novelfull.com"
    novel_name = "reincarnation-of-the-strongest-sword-god"
    dir_novel_downloads = f"downloads/{novel_name.lower()}"
    chapter_start = 49
    chapter_end = 51
    yield_chapter_urls = [
        (chapter_number, f"{source}/{novel_name}/chapter-{chapter_number:04d}.html")
        for chapter_number in range(chapter_start, chapter_end + 1)
    ]
    expected_download_chapter_args = [call(x) for _, x in yield_chapter_urls]
    download_filepaths = [
        f"{dir_novel_downloads}/chapter-{chapter_number:04d}.html"
        for chapter_number in range(chapter_start, chapter_end + 1)
    ]
    expected_open_args = [call(x, "w") for x in download_filepaths]
    chapter_content = [
        call(f"<html>Chapter {chapter_number} content</html>")
        for chapter_number in range(chapter_start, chapter_end + 1)
    ]
    expected_write_args = [call(x) for x in chapter_content]

    # Arrange mocks
    mock_crawler_instance = mock_crawler.return_value
    mock_crawler_instance.yield_chapter_urls.return_value = yield_chapter_urls
    mock_crawler_instance.download_chapter.side_effect = chapter_content

    # Act
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            [
                "download",
                novel_name,
                "--start",
                str(chapter_start),
                "--end",
                str(chapter_end),
            ],
        )

    # Assert
    assert result.exit_code == 0
    for x in download_filepaths:
        assert f"Downloaded chapter to {x}" in result.output

    # Check that the crawler was instantiated and called with the correct url
    mock_crawler.assert_called_once_with(novel_name)
    mock_crawler_instance.yield_chapter_urls.assert_called_once_with(
        chapter_start, chapter_end
    )
    assert (
        mock_crawler_instance.download_chapter.call_args_list
        == expected_download_chapter_args
    )

    # Ensure the directory was created
    mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

    # Check that the file was opened for writing and content was written
    assert mock_open_func.call_args_list == expected_open_args
    assert mock_open_func().write.call_args_list == expected_write_args

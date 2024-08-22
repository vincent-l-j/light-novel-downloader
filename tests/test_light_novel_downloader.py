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


def test_download():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            [
                "download",
                "reincarnation-of-the-strongest-sword-god",
                "--chapter",
                "15",
            ],
        )
        assert result.exit_code == 0
        assert result.output.startswith("Downloaded chapter")

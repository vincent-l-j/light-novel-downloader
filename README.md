# Light Novel Downloader

Welcome to the Light Novel Downloader repository!
This repository contains a script for downloading light novels.
The script is designed to be user-friendly and flexible,
allowing users to download their favourite light novels with ease.

## Requirements

- Python 3.8+
- `requests` library

## Installation

1. Install using pip:

   ```bash
   venv_name=venv
   python -m venv $venv_name
   source $venv_name/bin/activate
   python -m pip install light-novel-downloader
   # for some reason you need to activate the virtual env again on zsh
   source $venv_name/bin/activate
   ```

## Usage

1. **Run the script**:

   ```bash
   light-novel-downloader download <hyphenated-novel-name> --chapter <chapter-number>
   # e.g.
   light-novel-downloader download reincarnation-of-the-strongest-sword-god --chapter 1
   # to read the help docs
   light-novel-downloader --help
   # or
   light-novel-downloader -h
   ```

2. The downloaded novels will be saved in the `downloads` directory.

## License

This project is licensed under the [MIT License](LICENSE).

Thank you for using Light Novel Downloader!
If you have any questions or encounter issues, please open an
[issue](https://github.com/vincent-l-j/light-novel-downloader/issues).

---

Happy downloading and reading!

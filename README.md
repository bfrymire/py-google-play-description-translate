# Google Play App Description Translate

Google Cloud API has to be paid for monthly, Google Translate website, however... is free.

## Getting Started

```bash
pip install -r requirements.txt
```

`google_translate.py` is currently equipped to use Selenium Chromedriver as it's method to render a web page. If there's any interest in having the choice in which webdriver you want to use, open an issue.

1. Download Google Chromedriver.
	1. Make sure to download the correct version that works with your OS here: https://sites.google.com/a/chromium.org/chromedriver/
1. Install Chromedriver in your `PATH` so Python can use the webdriver.

## Usage

`google_translate.py` uses a command-line interface. To view all the arguments, run:

```bash
python google_translate.py --help
```

Basic usage:

```bash
python google_translate.py --output-language Spanish Portuguese
```

Running this will use the English text from `input.txt`, and translate it to Spanish and Portuguese, then dump the original text and translations to `output.txt`

## License

[MIT License](https://opensource.org/licenses/MIT)

Copyright (c) Brent Frymire
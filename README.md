# Gigantum Testing

Automation of Gigantum testing with Selenium.

## Installation

Make sure to create a Virtual Environment for this project.

```bash
$ python3 -m venv testenv
$ source testenv/bin/activate
$ pip3 install -r requirements.txt
```

Now, install the binary browser drivers.

```bash
# Web driver for Chrome/Chromium
$ brew install chromedriver

# Web driver for Firefox
$ brew install geckodriver
```

## Usage

See installation before running these commands.

To run ALL tests, using regular Chrome driver.
Note, this may take a while.

```
$ python3 driver.py
```

To run only example tests in headless mode.

```
$ python3 driver.py test_examples --headless
```

To run ALL tests using the Firefox driver
```
$ python3 driver.py --firefox
```


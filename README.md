# Gigantum Testing

Automation of Gigantum testing with Selenium.


## Installation

First, create and activate a Python Virtual Environment for this project.

```bash
$ python3 -m venv testenv
$ source testenv/bin/activate
$ pip3 install -r requirements.txt
```

Next, install the binary browser drivers, so that you can programmatically
interact with the browser.

```bash
# Web driver for Chrome/Chromium
$ brew install chromedriver

# Web driver for Firefox
$ brew install geckodriver
```


## Usage

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


## Organization

The file `driver.py` contains the main script to prepare, execute, and clean up test runs.

The directory `gigantum_tests` contains Python files containing individual tests.
Tests methods must be prefaced by `test_`, and should use the `assert` method for tests.

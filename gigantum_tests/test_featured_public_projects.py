# Builtin imports
import logging
import time

# Library imports
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Local packages
import testutils


def test_featured_public_projects(driver: selenium.webdriver, *args, **kwargs):
    """
    Test that featured public projects import and build successfully.

    Args:
        driver
    """
    # Project set up
    testutils.log_in(driver)
    time.sleep(2)
    testutils.remove_guide(driver)
    time.sleep(2)
    # Import featured public projects
    # TO DO - add in https://gigantum.com/gigantum-examples/allen-sdk-examples
    featured_public_projects = ["gigantum.com/meg297/military-expenditure-gdp-population",
                                "gigantum.com/billvb/fsw-telecoms-study",
                                "gigantum.com/randal/baltimore-sun-data-bridge-data"]
    for project in featured_public_projects:
        logging.info(f"Importing featured public project: {project}")
        driver.find_element_by_css_selector(".btn--import ~ .btn--import").click()
        time.sleep(2)
        driver.find_element_by_css_selector(".Import__input").send_keys(project)
        time.sleep(2)
        driver.find_element_by_css_selector("button ~ button").click()
        time.sleep(80)
        wait = selenium.webdriver.support.ui.WebDriverWait(driver, 200)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))
        assert driver.find_element_by_css_selector(".flex>.Stopped").is_displayed(), "Expected stopped container status"
        logging.info(f"Featured public project {project} was imported successfully")
        driver.find_element_by_css_selector(".SideBar__nav-item--labbooks").click()
        time.sleep(2)
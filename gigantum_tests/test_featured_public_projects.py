# Builtin imports
import logging
import time

# Library imports
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

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
        # Check that featured public project can be opened in JupyterLab
        driver.find_element_by_css_selector(".flex>.Stopped").click()
        time.sleep(10)
        driver.find_element_by_css_selector(".Btn--text").click()
        time.sleep(20)
        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[1])
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[title = code]")))
        assert driver.find_element_by_css_selector("[title = code]").is_displayed(), "Expected JupyterLab to open to code"
        logging.info("Opened JupyterLab to code successfully")
        # Switch back to project page
        driver.switch_to.window(window_handles[0])
        time.sleep(10)
        driver.find_element_by_css_selector(".SideBar__nav-item--labbooks").click()
        time.sleep(2)
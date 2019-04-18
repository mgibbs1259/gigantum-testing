import logging
import time

import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import testutils


def test_rstudio_session(driver: selenium.webdriver, *args, **kwargs):
    """
    Test the creation of a project with a python 2 minimal base.

    Args:
        driver
    """
    # Project set up
    testutils.log_in(driver)
    time.sleep(2)
    testutils.remove_guide(driver)
    time.sleep(2)
    testutils.create_project_without_base(driver)
    time.sleep(2)
    # R Tidy base
    testutils.add_rtidy_base(driver)
    # Wait until stopped container status
    wait = selenium.webdriver.support.ui.WebDriverWait(driver, 200)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))
    # Open JupyterLab
    logging.info("Opening JupyterLab")
    driver.find_element_by_css_selector(".ContainerStatus").click()
    time.sleep(5)
    driver.find_element_by_css_selector(".DevTools__btn--launch").click()
    time.sleep(10)
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[1])
    time.sleep(3)
    # Create R notebook
    logging.info("Creating R notebook")
    driver.find_element_by_css_selector("div[title = 'R']>.jp-LauncherCard-icon").click()
    time.sleep(3)
    # Import tidyverse and create graph
    logging.info("Importing tidyverse and creating a basic graph")
    code_input = driver.find_element_by_css_selector(".CodeMirror-line")
    actions = ActionChains(driver)
    logging.info("Import tidyverse")
    actions.move_to_element(code_input).click(code_input).send_keys('library(tidyverse)\n'
                                                                    "attach(mtcars)\n"
                                                                    "plot(wt, mpg)\n"
                                                                    "abline(lm(mpg~wt))\n"
                                                                    "title('Regression of MPG on Weight')").perform()
    driver.find_element_by_css_selector(".jp-RunIcon").click()
    time.sleep(10)



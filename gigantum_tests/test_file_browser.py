import logging
import time

import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import testutils


def test_file_drag_drop_project_file_browser(driver: selenium.webdriver, *args, **kwargs):
    """
    Test that a file can be dragged and dropped into code, input data,
    and output data in a project.

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
    testutils.add_py3_min_base(driver)
    wait = WebDriverWait(driver, 200)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))
    # Navigate to code
    logging.info("Navigating to Code")
    driver.find_element_by_css_selector("#code").click()
    time.sleep(2)
    logging.info("Dragging and dropping file into code")
    testutils.file_drag_drop(driver)
    time.sleep(3)

    code_first_file_title = driver.find_element_by_css_selector(".File__text div span").text
    assert code_first_file_title == 'sample-upload.txt', "Expected sample-upload.txt to be the first file in Code"

    # Navigate to input data
    logging.info("Navigating to Input Data")
    driver.find_element_by_css_selector("#inputData").click()
    logging.info("Dragging and dropping file into Input Data")
    testutils.file_drag_drop(driver)
    time.sleep(3)

    input_data_first_file_title = driver.find_element_by_css_selector(".File__text div span").text
    assert input_data_first_file_title == 'sample-upload.txt', "Expected sample-upload.txt to be the first file " \
                                                               "in Input Data"

    # Navigate to output data
    logging.info("Navigating to Output Data")
    driver.find_element_by_css_selector("#outputData").click()
    logging.info("Dragging and dropping file into Output Data")
    testutils.file_drag_drop(driver)
    time.sleep(3)

    output_data_first_file_title = driver.find_element_by_css_selector(".File__text div span").text
    assert output_data_first_file_title == 'sample-upload.txt', "Expected sample-upload.txt to be the first file " \
                                                                "in Output Data"


def test_file_drag_drop_dataset_file_browser(driver: selenium.webdriver, *args, **kwargs):
    """
    Test that a file can be dragged and dropped into data in a dataset.

    Args:
        driver
    """
    # Dataset set up
    testutils.log_in(driver)
    time.sleep(2)
    testutils.remove_guide(driver)
    time.sleep(2)
    testutils.create_dataset(driver)
    # Navigate to data
    logging.info("Navigating to Data")
    driver.find_element_by_css_selector("#data").click()
    logging.info("Dragging and dropping file into Data")
    testutils.file_drag_drop(driver, project=False)
    time.sleep(3)

    data_first_file_title = driver.find_element_by_css_selector(".File__text div span").text
    assert data_first_file_title == 'sample-upload.txt', "Expected sample-upload.txt to be the first file " \
                                                         "in Data"


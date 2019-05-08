import logging
import time

import selenium
from selenium.webdriver.common.by import By

import testutils


def test_project_file_browser(driver: selenium.webdriver, *args, **kwargs):
    """
    Test that a file can be dragged and dropped into code, input data,
    and output data in a project.

    Args:
        driver
    """
    # Project set up
    r = testutils.prep_py3_minimal_base(driver)
    username, project_title = r.username, r.project_name
    # Navigate to code
    logging.info("Navigating to Code")
    project_file_browser_elts = testutils.ProjectFileBrowserElements(driver)
    project_file_browser_elts.code_tab.wait().click()
    time.sleep(2)
    logging.info("Dragging and dropping file into code")
    testutils.file_drag_drop(driver)
    time.sleep(3)

    code_first_file_title = driver.find_element_by_css_selector(".File__text div span").text
    assert code_first_file_title == 'sample-upload.txt', "Expected sample-upload.txt to be the first file in Code"

    # Navigate to input data
    logging.info("Navigating to Input Data")
    project_file_browser_elts.input_data_tab.wait().click()
    logging.info("Dragging and dropping file into Input Data")
    testutils.file_drag_drop(driver)
    time.sleep(3)

    input_data_first_file_title = driver.find_element_by_css_selector(".File__text div span").text
    assert input_data_first_file_title == 'sample-upload.txt', \
        "Expected sample-upload.txt to be the first file in Input Data"

    # TODO - upload file to Output Data


def test_dataset_file_browser(driver: selenium.webdriver, *args, **kwargs):
    """
    Test that a file can be dragged and dropped into data in a dataset.

    Args:
        driver
    """
    # Dataset set up
    testutils.log_in(driver)
    testutils.GuideElements(driver).remove_guide()
    dataset_elts = testutils.DatasetElements(driver)
    dataset_elts.create_dataset(testutils.unique_dataset_name())
    # Navigate to data
    logging.info("Navigating to Data")
    dataset_elts.data_tab.wait().click()
    logging.info("Dragging and dropping file into Data")
    time.sleep(3)
    testutils.file_drag_drop(driver)
    time.sleep(3)

    data_first_file_title = driver.find_element_by_css_selector(".File__text div span").text
    assert data_first_file_title == 'sample-upload.txt', \
        "Expected sample-upload.txt to be the first file in Data"


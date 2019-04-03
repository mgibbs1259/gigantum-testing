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


def test_dataset(driver: selenium.webdriver, *args, **kwargs):
    """
    Test that dataset is created and published successfully.

    Args:
        driver
    """
    # dataset set up
    testutils.log_in(driver)
    time.sleep(2)
    testutils.remove_guide(driver)
    time.sleep(2)
    # create and publish datset
    dataset_title_local = testutils.create_dataset(driver)
    testutils.publish_dataset(driver)
    # check published dataset in the cloud
    dataset_title_cloud = driver.find_element_by_css_selector(".RemoteDatasets__panel-title:first-child span span").text

    assert dataset_title_local == dataset_title_cloud, "Expected dataset to be the first one in cloud tab"

    # clean up datasets local and remote
    logging.info("Removing project from cloud")
    driver.find_element_by_css_selector(".RemoteDatasets__icon--delete").click()
    driver.find_element_by_css_selector("#deleteInput").send_keys(dataset_title_local)
    time.sleep(2)
    driver.find_element_by_css_selector(".ButtonLoader").click()
    time.sleep(2)
    wait = WebDriverWait(driver, 200)
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".DeleteDataset")))
    dataset_title_cloud = driver.find_element_by_css_selector(".RemoteDatasets__panel-title:first-child span span").text

    assert dataset_title_local != dataset_title_cloud, "Expected dataset no longer the first one in cloud tab"

    logging.info("Removing project from local")
    driver.find_element_by_css_selector(".Datasets__nav-item--local").click()
    time.sleep(2)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".LocalDatasets__row--icons")))
    dataset_local = driver.find_element_by_css_selector(".LocalDatasets__panel-title:first-child span span").text

    assert dataset_title_local == dataset_local, "Expected project to be the first one in local tab"

    driver.find_element_by_css_selector(".LocalDatasets__panel-title").click()
    driver.find_element_by_css_selector(".ActionsMenu__btn").click()
    driver.find_element_by_css_selector(".ActionsMenu__item--delete").click()
    driver.find_element_by_css_selector("#deleteInput").send_keys(dataset_title_local)
    time.sleep(2)
    driver.find_element_by_css_selector(".ButtonLoader").click()
    time.sleep(2)
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".DeleteDataset")))
    dataset_local = driver.find_element_by_css_selector(".LocalDatasets__panel-title:first-child span span").text

    assert dataset_title_local != dataset_local, "Expected dataset no longer the first one in local tab"

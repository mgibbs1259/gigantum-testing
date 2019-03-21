# Builtin imports
import logging
import time
import os
import shutil
import subprocess

# Library imports
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Local packages
import testutils


def test_publish_sync_delete_project(driver: selenium.webdriver, *args, **kwargs):
    """
        Test that a project in Gigantum can be published, synced, and deleted.

        Args:
            driver
    """
    # Project set up
    username = testutils.log_in(driver)
    time.sleep(2)
    testutils.remove_guide(driver)
    time.sleep(2)
    testutils.create_project_without_base(driver)
    # Python 3 minimal base
    testutils.add_py3_min_base(driver)
    wait = WebDriverWait(driver, 200)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))
    # Grab project title
    full_project_title = driver.find_element_by_css_selector(".TitleSection__namespace-title").text
    project_title = full_project_title[full_project_title.index("/") + 1:].lstrip()
    # Publish project
    driver.find_element_by_css_selector(".BranchMenu__btn--sync--publish").click()
    driver.find_element_by_css_selector(".VisibilityModal__buttons > button").click()
    time.sleep(5)
    wait = selenium.webdriver.support.ui.WebDriverWait(driver, 200)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))
    assert "Added remote" in driver.find_element_by_css_selector(".Footer__message-title").text, "Expected 'Added remote' in footer"
    input_data_path = os.path.join(os.environ['GIGANTUM_HOME'], username,
                                   username, 'labbooks', project_title, 'input', 'file-3000000b.rando')


    # Add file to input data and sync project
    shutil.copy('testmaterial/file-3000000b.rando', input_data_path)
    driver.find_element_by_css_selector("#inputData").click()
    time.sleep(5)
    assert "file-3000000b.rando" in driver.find_element_by_css_selector(".File__text").text, "Expected file-3000000b.rando in input data"
    driver.find_element_by_css_selector(".BranchMenu__btn--sync").click()
    time.sleep(10)
    assert "Sync complete" in driver.find_element_by_css_selector(".Footer__message-list").text, "Expected 'Sync complete' in footer"
    driver.find_element_by_css_selector(".SideBar__icon--labbooks-selected").click()
    time.sleep(10)
    driver.find_element_by_css_selector(".Labbooks__nav-item--cloud").click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".RemoteLabbooks__panel-title")))
    # Delete cloud project
    driver.find_element_by_css_selector(".RemoteLabbooks__icon--delete").click()
    time.sleep(2)
    driver.find_element_by_css_selector("#deleteInput").send_keys(project_title)
    time.sleep(2)
    driver.find_element_by_css_selector(".ButtonLoader").click()
    time.sleep(8)
    assert project_title not in driver.find_element_by_css_selector(".RemoteLabbooks__panel-title").text, "Expected project to be removed from cloud tab"
    driver.find_element_by_css_selector(".Labbooks__nav-item--local").click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".LocalLabbooks__panel-title")))
    assert project_title in driver.find_element_by_css_selector(".LocalLabbooks__panel-title").text, "Expected project in local tab"

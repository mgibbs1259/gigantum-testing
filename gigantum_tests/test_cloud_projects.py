# Builtin imports
import logging
import time
import os
import shutil
from subprocess import Popen, PIPE

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
    logging.info("Publishing project")
    publish_elts = testutils.PublishProjectElements(driver)
    publish_elts.publish_project_button.click()
    publish_elts.publish_confirm_button.click()
    time.sleep(5)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))
    time.sleep(5)
    side_bar_elts = testutils.SideBarElements(driver)
    side_bar_elts.projects_icon.click()
    publish_elts.cloud_tab.click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".RemoteLabbooks__panel-title")))

    cloud_tab_first_project_title = driver.find_element_by_css_selector(
        ".RemoteLabbooks__panel-title:first-child span span").text
    assert cloud_tab_first_project_title == project_title, \
        "Expected project to be the first project in the cloud tab"

    project_path = os.path.join(os.environ['GIGANTUM_HOME'], username, username, 'labbooks', project_title)
    git_command1 = Popen(['git', 'remote', 'get-url', 'origin'], cwd=project_path, stdout=PIPE, stderr=PIPE)
    pub_stdout = git_command1.stdout.readline().decode('utf-8').strip()

    assert "https://" in pub_stdout, "Expected project on remote"

    publish_elts.local_tab.click()
    driver.find_element_by_css_selector(f"a[href='/projects/{username}/{project_title}']").click()

    # Add file to input data and sync project
    logging.info("Adding a file to the project")
    with open('/tmp/sample-upload.txt', 'w') as example_file:
        example_file.write('Sample Text')
    input_path = os.path.join(os.environ['GIGANTUM_HOME'], username, username, 'labbooks', project_title,
                              'input', 'file-3000000b.rando')
    shutil.copy(example_file.name, input_path)
    time.sleep(5)
    driver.find_element_by_css_selector("#inputData").click()
    time.sleep(2)
    logging.info("Syncing project")
    publish_elts.sync_project_button.click()
    time.sleep(2)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))

    sync_message = driver.find_element_by_css_selector(".Footer__message-list").text
    assert "Sync complete" in sync_message, "Expected 'Sync complete' in footer"

    side_bar_elts.projects_icon.click()
    publish_elts.cloud_tab.click()
    time.sleep(2)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".RemoteLabbooks__panel-title")))

    # Delete cloud project
    publish_elts.delete_project_button.click()
    time.sleep(2)
    publish_elts.delete_project_input.send_keys(project_title)
    time.sleep(2)
    publish_elts.delete_confirm_button.click()
    time.sleep(5)

    assert cloud_tab_first_project_title != project_title, \
        "Expected project to not be the first project in the cloud tab"

    driver.find_element_by_css_selector(".Labbooks__nav-item--local").click()
    time.sleep(2)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".LocalLabbooks__panel-title")))

    assert project_title in driver.find_element_by_css_selector(".LocalLabbooks__panel-title:first-child span span").text, "Expected project in local tab"

    git_command2 = Popen(['git', 'remote', 'get-url', 'origin'], cwd=project_path, stdout=PIPE, stderr=PIPE)
    del_stderr = git_command2.stderr.readline().decode('utf-8').strip()

    assert "fatal" in del_stderr, "Expected project to be deleted from remote"

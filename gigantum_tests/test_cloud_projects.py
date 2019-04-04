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
    project_title = testutils.create_project_without_base(driver)
    # Python 3 minimal base
    testutils.add_py3_min_base(driver)
    wait = WebDriverWait(driver, 200)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))

    # Publish project
    logging.info("Publishing private project")
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

    cloud_tab_first_project_title_publish = driver.find_element_by_css_selector(
        ".RemoteLabbooks__panel-title:first-child span span").text
    assert cloud_tab_first_project_title_publish == project_title, \
        "Expected project to be the first project in the cloud tab"

    project_path = os.path.join(os.environ['GIGANTUM_HOME'], username, username,
                                'labbooks', project_title)
    git_get_remote_command_1 = Popen(['git', 'remote', 'get-url', 'origin'],
                                     cwd=project_path, stdout=PIPE, stderr=PIPE)
    pub_stdout = git_get_remote_command_1.stdout.readline().decode('utf-8').strip()

    assert "https://" in pub_stdout, f"Expected to see a remote set for project, but got {pub_stdout}"

    publish_elts.local_tab.click()
    driver.find_element_by_css_selector(f"a[href='/projects/{username}/{project_title}']").click()

    # Add file to input data and sync project
    logging.info("Adding a file to the project")
    with open('/tmp/sample-upload.txt', 'w') as example_file:
        example_file.write('Sample Text')
    input_path = os.path.join(os.environ['GIGANTUM_HOME'], username, username, 'labbooks', project_title,
                              'input')
    shutil.copy(example_file.name, input_path)
    time.sleep(2)
    logging.info(f"Syncing {project_title}")
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

    # Test that the project is not the first project in the cloud tab
    cloud_tab_first_project_title_delete = driver.find_element_by_css_selector(
        ".RemoteLabbooks__panel-title:first-child span span").text
    assert cloud_tab_first_project_title_delete != project_title, \
        "Expected project to not be the first project in the cloud tab"

    publish_elts.local_tab.click()
    time.sleep(2)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".LocalLabbooks__panel-title")))

    # Test that the project is the first project in the local tab
    local_tab_first_project_title = driver.find_element_by_css_selector(
        ".LocalLabbooks__panel-title:first-child span span").text
    assert local_tab_first_project_title == project_title, \
        "Expected project to be the first project in the local tab"

    git_get_remote_command_2 = Popen(['git', 'remote', 'get-url', 'origin'],
                                     cwd=project_path, stdout=PIPE, stderr=PIPE)
    del_stderr = git_get_remote_command_2.stderr.readline().decode('utf-8').strip()

    assert "fatal" in del_stderr, f"Expected to not see a remote set for project, but got {del_stderr}"


def test_publish_collaborator(driver: selenium.webdriver, *args, ** kwargs):
    """
        Test that a project in Gigantum can be published, shared with a collaborator, and imported by the collaborator.

        Args:
            driver
    """
    # Project set up
    username = testutils.log_in(driver)
    time.sleep(2)
    testutils.remove_guide(driver)
    time.sleep(2)
    project_title = testutils.create_project_without_base(driver)
    # Python 3 minimal base
    testutils.add_py3_min_base(driver)
    wait = WebDriverWait(driver, 200)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))

    # Publish project
    publish_elts = testutils.PublishProjectElements(driver)
    publish_elts.publish_project_button.click()
    publish_elts.publish_confirm_button.click()
    time.sleep(5)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))

    # Add collaborator
    logging.info("Adding a collaborator to private project")
    publish_elts.collaborators_button.click()
    time.sleep(3)
    credentials = open('credentials.txt').readlines()
    username2, password2 = credentials[2], credentials[3]
    publish_elts.collaborators_input.send_keys(username2)
    publish_elts.add_collaborators_button.click()
    time.sleep(3)
    publish_elts.close_collaborators_button.click()
    logging.info("Logging out")
    time.sleep(2)
    driver.find_element_by_css_selector("#username").click()
    time.sleep(2)
    driver.find_element_by_css_selector("#logout").click()
    time.sleep(3)
    driver.quit()

    # Collaborator checks that the project is in the cloud tab and that the project imports successfully
    logging.info("Switching to new driver for collaborator")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--incognito")
    driver2 = webdriver.Chrome(chrome_options=chrome_options)
    driver2.implicitly_wait(5)
    driver2.set_window_size(1440, 1000)
    driver2.get("http://localhost:10000/projects/local#")
    logging.info("Logging in")
    auth0_elts = testutils.Auth0LoginElements(driver2)
    auth0_elts.login_green_button.click()
    time.sleep(2)
    auth0_elts.username_input.click()
    auth0_elts.username_input.send_keys(username2)
    auth0_elts.password_input.click()
    auth0_elts.password_input.send_keys(password2)
    driver2.find_element_by_css_selector(".auth0-lock-submit").click()
    time.sleep(5)
    testutils.remove_guide(driver2)
    logging.info("Collaborator importing shared project")
    driver2.find_element_by_css_selector(".Labbooks__nav-item--cloud").click()
    time.sleep(2)
    wait2 = WebDriverWait(driver2, 200)
    wait2.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".RemoteLabbooks__panel-title")))
    assert project_title in driver2.find_element_by_css_selector(".RemoteLabbooks__panel-title:first-child span span").text, "Expected shared project to in cloud tab"
    driver2.find_element_by_css_selector(".RemoteLabbooks__icon--cloud-download").click()
    wait2.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))
    assert project_title in driver2.find_element_by_css_selector(".TitleSection__namespace-title").text, "After import, expected shared project page"
    logging.info("Logging out")
    time.sleep(2)
    driver2.find_element_by_css_selector("#username").click()
    time.sleep(2)
    driver2.find_element_by_css_selector("#logout").click()
    time.sleep(3)
    driver2.quit()

    # Owner deletes cloud project
    logging.info("Switching to new driver for owner")
    lines2 = open('credentials.txt').readlines()
    username3, password3 = lines2[0], lines2[1]
    driver3 = webdriver.Chrome(chrome_options=chrome_options)
    driver3.implicitly_wait(5)
    driver3.set_window_size(1440, 1000)
    driver3.get("http://localhost:10000/projects/local#")
    logging.info("Logging in")
    auth0_elts = testutils.Auth0LoginElements(driver3)
    auth0_elts.login_green_button.click()
    time.sleep(2)
    auth0_elts.username_input.click()
    auth0_elts.username_input.send_keys(username3)
    auth0_elts.password_input.click()
    auth0_elts.password_input.send_keys(password3)
    time.sleep(10)
    testutils.remove_guide(driver3)
    logging.info("Owner deleting shared project")
    driver3.find_element_by_css_selector(".SideBar__icon--labbooks-selected").click()
    driver3.find_element_by_css_selector(".Labbooks__nav-item--cloud").click()
    time.sleep(2)
    wait3 = selenium.webdriver.support.ui.WebDriverWait(driver3, 200)
    wait3.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".RemoteLabbooks__panel-title")))
    driver3.find_element_by_css_selector(".RemoteLabbooks__icon--delete").click()
    time.sleep(2)
    driver3.find_element_by_css_selector("#deleteInput").send_keys(project_title)
    time.sleep(2)
    driver3.find_element_by_css_selector(".ButtonLoader").click()
    time.sleep(5)
    git_command2 = Popen(['git', 'remote', 'get-url', 'origin'], cwd=project_path, stdout=PIPE, stderr=PIPE)
    del_stderr = git_command2.stderr.readline().decode('utf-8').strip()
    assert "fatal" in del_stderr, "Expected project to be deleted from remote"




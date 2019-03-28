# Builtin imports
import logging
import time
import os
import shutil
from subprocess import Popen, PIPE
import sys

# Library imports
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Local packages
import testutils

'''
def test_publish_sync_delete_project(driver: selenium.webdriver, *args, **kwargs):
    """
        #Test that a project in Gigantum can be published, synced, and deleted.

        #Args:
            #driver
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
    driver.find_element_by_css_selector(".BranchMenu__btn--sync--publish").click()
    driver.find_element_by_css_selector(".VisibilityModal__buttons > button").click()
    time.sleep(5)
    wait = selenium.webdriver.support.ui.WebDriverWait(driver, 200)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))
    time.sleep(5)
    driver.find_element_by_css_selector(".SideBar__icon--labbooks-selected").click()
    driver.find_element_by_css_selector(".Labbooks__nav-item--cloud").click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".RemoteLabbooks__panel-title")))
    assert project_title in driver.find_element_by_css_selector(".RemoteLabbooks__panel-title:first-child span span").text, "Expected project to be in cloud tab"
    project_path = os.path.join(os.environ['GIGANTUM_HOME'], username, username, 'labbooks', project_title)
    git_command1 = Popen(['git', 'remote', 'get-url', 'origin'], cwd=project_path, stdout=PIPE, stderr=PIPE)
    pub_stdout = git_command1.stdout.readline().decode('utf-8').strip()
    assert "https://" in pub_stdout, "Expected project on remote"
    driver.find_element_by_css_selector(".Labbooks__nav-item--local").click()
    driver.find_element_by_css_selector(f"a[href='/projects/{username}/{project_title}']").click()

    # Add file to input data and sync project
    logging.info("Adding a file to the project")
    input_path = os.path.join(os.environ['GIGANTUM_HOME'], username, username, 'labbooks', project_title,
                              'input', 'file-3000000b.rando')
    shutil.copy('testmaterial/file-3000000b.rando', input_path)
    time.sleep(5)
    driver.find_element_by_css_selector("#inputData").click()
    time.sleep(2)
    assert "file-3000000b.rando" in driver.find_element_by_css_selector(".File__text").text, "Expected file-3000000b.rando in input data"
    logging.info("Syncing project")
    driver.find_element_by_css_selector(".BranchMenu__btn--sync").click()
    time.sleep(2)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))
    assert "Sync complete" in driver.find_element_by_css_selector(".Footer__message-list").text, "Expected 'Sync complete' in footer"
    driver.find_element_by_css_selector(".SideBar__icon--labbooks-selected").click()
    driver.find_element_by_css_selector(".Labbooks__nav-item--cloud").click()
    time.sleep(2)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".RemoteLabbooks__panel-title")))

    # Delete cloud project
    driver.find_element_by_css_selector(".RemoteLabbooks__icon--delete").click()
    time.sleep(2)
    driver.find_element_by_css_selector("#deleteInput").send_keys(project_title)
    time.sleep(2)
    driver.find_element_by_css_selector(".ButtonLoader").click()
    time.sleep(5)
    assert project_title not in driver.find_element_by_css_selector(".RemoteLabbooks__panel-title:first-child span span").text, "Expected project to be removed from cloud tab"
    driver.find_element_by_css_selector(".Labbooks__nav-item--local").click()
    time.sleep(2)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".LocalLabbooks__panel-title")))
    assert project_title in driver.find_element_by_css_selector(".LocalLabbooks__panel-title:first-child span span").text, "Expected project in local tab"
    git_command2 = Popen(['git', 'remote', 'get-url', 'origin'], cwd=project_path, stdout=PIPE, stderr=PIPE)
    del_stderr = git_command2.stderr.readline().decode('utf-8').strip()
    assert "fatal" in del_stderr, "Expected project to be deleted from remote"
'''

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
    driver.find_element_by_css_selector(".BranchMenu__btn--sync--publish").click()
    driver.find_element_by_css_selector(".VisibilityModal__buttons > button").click()
    time.sleep(5)
    wait = selenium.webdriver.support.ui.WebDriverWait(driver, 200)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))
    project_path = os.path.join(os.environ['GIGANTUM_HOME'], username, username, 'labbooks', project_title)
    git_command1 = Popen(['git', 'remote', 'get-url', 'origin'], cwd=project_path, stdout=PIPE, stderr=PIPE)
    pub_stdout = git_command1.stdout.readline().decode('utf-8').strip()
    assert "https://" in pub_stdout, "Expected project on remote"

    # Add collaborator
    time.sleep(3)
    driver.find_element_by_css_selector(".Collaborators__btn").click()
    time.sleep(3)
    lines = open('credentials.txt').readlines()
    username2, password2 = lines[2], lines[3]
    driver.find_element_by_css_selector(".CollaboratorsModal__input--collaborators").send_keys(username2)
    driver.find_element_by_css_selector(".CollaboratorsModal__btn--add").click()
    time.sleep(5)
    driver.find_element_by_css_selector(".Modal__close").click()
    time.sleep(2)
    driver.find_element_by_css_selector("#username").click()
    time.sleep(2)
    driver.find_element_by_css_selector("#logout").click()
    time.sleep(3)
    driver.quit()

    # Collaborator checks that the project is in the cloud tab and that the project imports successfully
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
    driver2.find_element_by_css_selector(".Labbooks__nav-item--cloud").click()
    time.sleep(2)
    wait2 = WebDriverWait(driver2, 200)
    wait2.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".RemoteLabbooks__panel-title")))
    assert project_title in driver2.find_element_by_css_selector(".RemoteLabbooks__panel-title:first-child span span").text, "Expected shared project to in cloud tab"
    driver2.find_element_by_css_selector(".RemoteLabbooks__icon--cloud-download").click()
    wait2.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))
    assert project_title in driver2.find_element_by_css_selector(".TitleSection__namespace-title").text, "After import, expected shared project page"
    time.sleep(2)
    driver2.find_element_by_css_selector("#username").click()
    time.sleep(2)
    driver2.find_element_by_css_selector("#logout").click()
    time.sleep(3)
    driver2.quit()

    # Owner deletes cloud project
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
    time.sleep(5)
    testutils.remove_guide(driver3)
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



import logging
import time
import os
import shutil

import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import testutils
from testutils import graphql


def test_create_local_branch(driver: selenium.webdriver, *args, **kwargs):
    """
    Test the creation of a local branch.
    """
    r = testutils.prep_py3_minimal_base(driver)
    username, project_title = r.username, r.project_name
    branch_elts = testutils.BranchElements(driver)
    branch_elts.create_local_branch("test-branch")
    time.sleep(8)
    logging.info("Checking that you are on the new branch and that the new branch is local only")

    assert branch_elts.upper_left_branch_name.find().text == "test-branch", \
        "Expected to be on test-branch, upper left"
    assert branch_elts.upper_left_branch_local_only.find(), "Expected test-branch to be local only, upper left"

    branch_elts.manage_branches_button.wait().click()
    time.sleep(2)

    assert branch_elts.manage_branches_branch_name.find().text == "test-branch", \
        "Expected to be on test-branch, manage branches"
    assert branch_elts.manage_branches_local_only.find(), "Expected test-branch to be local only, manage branches"


def test_delete_file_local_branch(driver: selenium.webdriver, *args, **kwargs):
    """
    Test that a file created on the master branch, deleted in a local branch, and then merged back into the
    master branch does not appear in the master branch.
    """
    r = testutils.prep_py3_minimal_base(driver)
    username, project_title = r.username, r.project_name
    logging.info(f"Navigating to Input Data")
    driver.get(f"{os.environ['GIGANTUM_HOST']}/projects/{username}/{project_title}/inputData")
    time.sleep(2)
    logging.info(f"Adding a file to the master branch of project {project_title}")
    with open('/tmp/sample-upload.txt', 'w') as example_file:
        example_file.write('Sample Text')
    input_path = os.path.join(os.environ['GIGANTUM_HOME'], username, username, 'labbooks', project_title, 'input')
    shutil.copy(example_file.name, input_path)
    time.sleep(8)
    branch_elts = testutils.BranchElements(driver)
    branch_elts.create_local_branch("test-branch")
    time.sleep(8)
    logging.info(f"Deleting file in test-branch")
    file_browser_elts = testutils.FileBrowserElements(driver)
    file_browser_elts.check_file_check_box.find().click()
    file_browser_elts.delete_file_button.wait().click()
    file_browser_elts.confirm_delete_file_button.wait().click()
    time.sleep(4)
    logging.info(f"Switching to master branch")
    branch_elts.upper_left_branch_drop_down_button.find().click()
    branch_elts.upper_left_first_branch_button.wait().click()
    time.sleep(4)
    logging.info(f"Merging test-branch into master branch")
    branch_elts.manage_branches_button.wait().click()
    branch_container_hover = ActionChains(driver).move_to_element(branch_elts.manage_branches_branch_container.find())
    branch_container_hover.perform()
    branch_elts.manage_branches_merge_branch_button.wait().click()
    time.sleep(2)
    branch_elts.manage_branches_confirm_merge_branch_button.wait().click()
    time.sleep(8)
    logging.info(f"Checking that file deleted in test-branch does not appear in master branch")

    assert file_browser_elts.file_browser_empty.find(), "Expected sample-upload.txt to not appear in master branch"


def test_file_favorite_local_branch(driver: selenium.webdriver, *args, **kwargs):
    """
    Test that a file created on the master branch, favorited in a local branch, and then merged back into the
    master branch is favorited in the master branch.
    """
    r = testutils.prep_py3_minimal_base(driver)
    username, project_title = r.username, r.project_name
    logging.info(f"Navigating to Input Data")
    driver.get(f"{os.environ['GIGANTUM_HOST']}/projects/{username}/{project_title}/inputData")
    time.sleep(2)
    logging.info(f"Adding a file to the master branch of project {project_title}")
    with open('/tmp/sample-upload.txt', 'w') as example_file:
        example_file.write('Sample Text')
    input_path = os.path.join(os.environ['GIGANTUM_HOME'], username, username, 'labbooks', project_title, 'input')
    shutil.copy(example_file.name, input_path)
    time.sleep(8)
    branch_elts = testutils.BranchElements(driver)
    branch_elts.create_local_branch("test-branch")
    time.sleep(8)
    logging.info(f"Favoriting file in test-branch")
    file_browser_elts = testutils.FileBrowserElements(driver)
    file_browser_elts.favorite_file_button.find().click()
    logging.info(f"Switching to master branch")
    branch_elts.upper_left_branch_drop_down_button.find().click()
    branch_elts.upper_left_first_branch_button.wait().click()
    time.sleep(4)
    logging.info(f"Merging test-branch into master branch")
    branch_elts.manage_branches_button.wait().click()
    branch_container_hover = ActionChains(driver).move_to_element(branch_elts.manage_branches_branch_container.find())
    branch_container_hover.perform()
    branch_elts.manage_branches_merge_branch_button.wait().click()
    time.sleep(2)
    branch_elts.manage_branches_confirm_merge_branch_button.wait().click()
    time.sleep(8)
    logging.info(f"Checking that file favorited in test-branch is favorited in master branch")

    assert file_browser_elts.favorite_file_button.find(), "Expected sample-upload.txt to be favorited in master branch"

















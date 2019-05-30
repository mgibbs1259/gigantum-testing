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
    driver.get(f"{os.environ['GIGANTUM_HOST']}/projects/{username}/{project_title}")
    time.sleep(4)
    branch_elts = testutils.BranchElements(driver)
    branch_elts.create_local_branch("test-branch")
    time.sleep(4)
    logging.info("Checking that you are on the new branch and that the new branch is local only")

    assert branch_elts.upper_left_branch_name.find().text == "my-test-branch", \
        "Expected to be on my-test-branch, upper left"
    assert branch_elts.upper_left_branch_local_only.find(), "Expected my-test-branch to be local only, upper left"

    branch_elts.manage_branches_button.wait().click()
    time.sleep(2)

    assert branch_elts.manage_branches_branch_name.find().text == "my-test-branch", \
        "Expected to be on my-test-branch, manage branches"
    assert branch_elts.manage_branches_local_only.find(), "Expected my-test-branch to be local only, manage branches"


def test_delete_file_local_branch(driver: selenium.webdriver, *args, **kwargs):
    """
    Test that files created on the master branch, deleted in a local branch, and then merged back into the
    master branch do not appear in the master branch.
    """
    r = testutils.prep_py3_minimal_base(driver)
    username, project_title = r.username, r.project_name
    driver.get(f"{os.environ['GIGANTUM_HOST']}/projects/{username}/{project_title}")
    time.sleep(4)
    logging.info(f"Adding a file to the master branch of project {project_title}")
    with open('/tmp/sample-upload.txt', 'w') as example_file:
        example_file.write('Sample Text')
    input_path = os.path.join(os.environ['GIGANTUM_HOME'], username, username, 'labbooks', project_title, 'input')
    shutil.copy(example_file.name, input_path)
    branch_elts = testutils.BranchElements(driver)
    branch_elts.create_local_branch("test-branch")
    logging.info(f"Deleting file in test-branch")
    file_browser_elts = testutils.FileBrowserElements(driver)
    file_browser_elts.delete_file_button.find().click()
    file_browser_elts.confirm_delete_file_button.wait().click()
    time.sleep(2)
    logging.info(f"Switching to master branch")
    branch_elts.upper_left_branch_drop_down_button.find().click()
    branch_elts.upper_left_first_branch_button.wait().click()
    logging.info(f"Merging test-branch into master branch")
    branch_elts.manage_branches_button.wait().click()
    hover = ActionChains(driver).move_to_element(branch_elts.manage_branches_branch_container)
    hover.perform()
    branch_elts.manage_branches_merge_branch_button.find().click()
    branch_elts.manage_branches_confirm_merge_branch_button.wait().click()
    time.sleep(8)
    logging.info(f"Checking that file deleted in test-branch does not appear on master branch")
    first_file = file_browser_elts.file_information.find().text

    assert first_file != "sample-upload.txt", f"Expected {first_file} to not appear in master branch"
















# Builtin imports
import logging
import time
import os

# Library imports
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Local packages
import testutils
from testutils.graphql import create_py3_minimal_project


def test_create_local_branch(driver: selenium.webdriver, *args, **kwargs):
    """
    Test the creation of a local branch.

    Args:
        driver
    """
    # Project set up
    username = testutils.log_in(driver)
    time.sleep(2)
    testutils.remove_guide(driver)

    owner, proj_name = create_py3_minimal_project(testutils.unique_project_name())
    driver.get(f'{os.environ["GIGANTUM_HOST"]}/projects/{username}/{proj_name}')

    time.sleep(4)

    logging.info("Creating a new branch")
    branch_elts = testutils.BranchElements(driver)
    branch_elts.create_branch_button.click()
    branch_elts.branch_name_input.send_keys("my-test-branch")
    branch_elts.create_button.click()
    time.sleep(5)
    logging.info("Checking that the new branch is local only")

    upper_left_branch_name = driver.find_element_by_css_selector(".BranchMenu__dropdown-text").text
    upper_left_local_only = driver.find_element_by_css_selector(
        '.BranchMenu__dropdown-btn>div[data-tooltip="Local only"]')
    assert upper_left_branch_name == "my-test-branch", "Expected to be on my-test-branch, upper left"
    assert upper_left_local_only, "Expected my-test-branch to be local only, upper left"

    # Open manage branches
    branch_elts.manage_branches_button.click()
    time.sleep(2)

    manage_branches_branch_name = driver.find_element_by_css_selector(".Branches__branchname").text
    manage_branches_local_only = driver.find_element_by_css_selector(
        '.Branches__details>div[data-tooltip="Local only"]')
    assert manage_branches_branch_name == "my-test-branch", "Expected to be on my-test-branch, manage branches"
    assert manage_branches_local_only, "Expected my-test-branch to be local only, manage branches"



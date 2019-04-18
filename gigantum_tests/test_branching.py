# Builtin imports
import time

# Library imports
import selenium
from selenium.webdriver.common.by import By

# Local packages
import testutils


def test_create_local_branch(driver: selenium.webdriver, *args, **kwargs):
    """
    Test the creation of a local branch.

    Args:
        driver
    """
    # Create project
    testutils.log_in_remove_guide(driver)
    testutils.create_project_without_base(driver)
    testutils.add_py3_min_base(driver)
    # Create a local branch
    test_branch_name = testutils.create_local_branch(driver)

    # Check branch is local only, upper left
    upper_left_branch_name = driver.find_element_by_css_selector(".BranchMenu__dropdown-text").text
    upper_left_local_only = driver.find_element_by_css_selector(
        '.BranchMenu__dropdown-btn>div[data-tooltip="Local only"]')
    assert upper_left_branch_name == test_branch_name, f"Expected to be on {test_branch_name}, upper left"
    assert upper_left_local_only, f"Expected {test_branch_name} to be local only, upper left"

    branch_elts = testutils.BranchElements(driver)
    branch_elts.manage_branches_button.click()
    time.sleep(2)

    # Check branch is local only, manage branches
    manage_branches_branch_name = driver.find_element_by_css_selector(".Branches__branchname").text
    manage_branches_local_only = driver.find_element_by_css_selector(
        '.Branches__details>div[data-tooltip="Local only"]')
    assert manage_branches_branch_name == test_branch_name, f"Expected to be on {test_branch_name}, manage branches"
    assert manage_branches_local_only, f"Expected {test_branch_name} to be local only, manage branches"



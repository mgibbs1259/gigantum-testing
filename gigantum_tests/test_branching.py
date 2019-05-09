import logging
import time
import os

import selenium
from selenium.webdriver.common.by import By

import testutils
from testutils import graphql


def test_create_local_branch(driver: selenium.webdriver, *args, **kwargs):
    """
    Test the creation of a local branch.
    """
    testutils.log_in(driver)
    time.sleep(2)
    testutils.GuideElements(driver).remove_guide()
    owner, proj_name = graphql.create_py3_minimal_project(testutils.unique_project_name())
    driver.get(f"{os.environ['GIGANTUM_HOST']}/projects/{owner}/{proj_name}")
    time.sleep(4)
    branch_elts = testutils.BranchElements(driver)
    branch_elts.create_local_branch("my-test-branch")
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



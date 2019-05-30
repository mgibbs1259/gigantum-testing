import logging
import time
import os

import selenium
from selenium.webdriver.common.by import By

import testutils
from testutils import graphql


def test_merge_conflict_project_use_theirs(driver: selenium.webdriver, *args, **kwargs):
    """
    Test a merge conflict in a project in which the owner resolves it with 'use theirs.'
    """
    # Owner creates a project, adds a file, and publishes the project
    r = testutils.prep_py3_minimal_base(driver)
    username, project_title = r.username, r.project_name
    driver.get(f'{os.environ["GIGANTUM_HOST"]}/projects/{username}/{project_title}/inputData')
    time.sleep(3)
    file_browser_elts = testutils.FileBrowserElements(driver)
    file_browser_elts.drag_drop_file_in_drop_zone()
    cloud_project_elts = testutils.CloudProjectElements(driver)
    cloud_project_elts.publish_private_project(project_title)
    # Owner adds a collaborator and logs out
    cloud_project_elts.add_collaborator_with_permissions(project_title, permissions="admin")
    side_bar_elts = testutils.SideBarElements(driver)
    side_bar_elts.do_logout()
    # Collaborator logs in and adds a file with the same title, but different content


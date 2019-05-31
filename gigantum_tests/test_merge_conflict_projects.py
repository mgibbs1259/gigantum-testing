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
    # Owner creates a project, publishes it, adds a collaborator, and logs out
    r = testutils.prep_py3_minimal_base(driver)
    username, project_title = r.username, r.project_name
    cloud_project_elts = testutils.CloudProjectElements(driver)
    cloud_project_elts.publish_private_project(project_title)
    collaborator = cloud_project_elts.add_collaborator_with_permissions(project_title, permissions="admin")
    side_bar_elts = testutils.SideBarElements(driver)
    side_bar_elts.do_logout(username)

    # Collaborator logs in and imports the cloud project
    logging.info(f"Logging in as {collaborator}")
    testutils.log_in(driver, user_index=1)
    time.sleep(2)
    try:
        testutils.GuideElements.remove_guide(driver)
    except:
        pass
    time.sleep(2)
    logging.info(f"Navigating to {collaborator}'s Cloud tab")
    driver.get(f"{os.environ['GIGANTUM_HOST']}/projects/cloud")
    time.sleep(2)
    cloud_project_elts.first_cloud_project.wait(90)
    cloud_project_elts.import_first_cloud_project_button.find().click()
    container_elts = testutils.ContainerElements(driver)
    container_elts.container_status_stopped.wait(90)

    # Collaborator adds a file, syncs, and logs out
    driver.get(f'{os.environ["GIGANTUM_HOST"]}/projects/{username}/{project_title}/inputData')
    time.sleep(2)
    file_browser_elts = testutils.FileBrowserElements(driver)
    file_browser_elts.drag_drop_file_in_drop_zone()
    cloud_project_elts.sync_cloud_project(project_title)
    side_bar_elts.do_logout(collaborator)

    # Owner logs in, adds a file with the same name, but different content, and syncs
    logging.info(f"Logging in as {username}")
    testutils.log_in(driver)
    time.sleep(2)
    try:
        testutils.GuideElements.remove_guide(driver)
    except:
        pass
    time.sleep(2)
    logging.info(f"Navigating to {username}'s Input Data tab")
    driver.get(f'{os.environ["GIGANTUM_HOST"]}/projects/{username}/{project_title}/inputData')
    time.sleep(2)
    file_browser_elts.drag_drop_file_in_drop_zone(file_content="Merge Conflict")
    cloud_project_elts.sync_cloud_project(project_title)
    cloud_project_elts.merge_conflict_use_mine_button.wait().click()
    time.sleep(1000)

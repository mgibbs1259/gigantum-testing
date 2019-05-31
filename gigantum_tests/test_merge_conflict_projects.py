import logging
import time
import os

import selenium
from selenium.webdriver.common.by import By

import testutils
from testutils import graphql


def prep_merge_conflict(driver: selenium.webdriver, *args, **kwargs):
    """
    Prepare a merge conflict in a project.
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
    file_browser_elts.drag_drop_file_in_drop_zone(file_content="Collaborator")
    cloud_project_elts.sync_cloud_project(project_title)
    side_bar_elts.do_logout(collaborator)

    # Owner logs in and navigates to Input Data
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
    file_browser_elts = testutils.FileBrowserElements(driver)
    file_browser_elts.drag_drop_file_in_drop_zone(file_content="Owner")
    cloud_project_elts = testutils.CloudProjectElements(driver)
    cloud_project_elts.sync_cloud_project(project_title)
    return username, project_title, collaborator


def test_use_mine_merge_conflict_project(driver: selenium.webdriver, *args, **kwargs):
    """
    Test a merge conflict in a project in which the owner resolves it with 'Use Mine.'
    """
    # Prepare merge conflict
    username, project_title, collaborator = prep_merge_conflict(driver)
    # Owner resolves the merge conflict with 'Use Mine'
    cloud_project_elts = testutils.CloudProjectElements(driver)
    cloud_project_elts.merge_conflict_use_mine_button.wait(90).click()
    cloud_project_elts.sync_cloud_project_message.wait()
    # Check that merge conflict resolves to 'Use Mine'
    file_path = os.path.join(os.environ['GIGANTUM_HOME'], username, username, 'labbooks',
                             project_title, 'input', 'sample-upload.txt')
    with open(file_path, "r") as resolve_merge_conflict_file:
        resolve_merge_conflict_file = resolve_merge_conflict_file.read()

    assert resolve_merge_conflict_file == "Owner", \
        f"Merge did not resolve to 'Use Mine' expected to see 'Owner' in file, " \
        f"but instead got {resolve_merge_conflict_file}"


def test_use_theirs_merge_conflict_project(driver: selenium.webdriver, *args, **kwargs):
    """
    Test a merge conflict in a project in which the owner resolves it with 'Use Theirs.'
    """
    # Prepare merge conflict
    username, project_title, collaborator = prep_merge_conflict(driver)
    # Owner uploads file, syncs, and resolves the merge conflict with 'Use Theirs'
    cloud_project_elts = testutils.CloudProjectElements(driver)
    cloud_project_elts.merge_conflict_use_theirs_button.wait(90).click()
    cloud_project_elts.sync_cloud_project_message.wait()
    # Check that merge conflict resolves to 'Use Theirs'
    file_path = os.path.join(os.environ['GIGANTUM_HOME'], username, username, 'labbooks',
                             project_title, 'input', 'sample-upload.txt')
    with open(file_path, "r") as resolve_merge_conflict_file:
        resolve_merge_conflict_file = resolve_merge_conflict_file.read()

    assert resolve_merge_conflict_file == "Collaborator", \
        f"Merge did not resolve to 'Use Mine' expected to see 'Collaborator' in file, " \
        f"but instead got {resolve_merge_conflict_file}"




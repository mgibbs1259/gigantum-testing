import logging
import time
import os
from subprocess import Popen, PIPE

import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import testutils
from testutils import graphql


def test_publish_sync_delete_project(driver: selenium.webdriver, *args, **kwargs):
    """
        Test that a project in Gigantum can be published, synced, and deleted.
    """
    # Create and publish project
    r = testutils.prep_py3_minimal_base(driver)
    username, project_title = r.username, r.project_name
    cloud_project_elts = testutils.CloudProjectElements(driver)
    cloud_project_elts.publish_private_project(project_title)
    logging.info(f"Navigating to {username}'s Cloud tab")
    driver.get(f"{os.environ['GIGANTUM_HOST']}/projects/cloud")
    cloud_project_elts.first_cloud_project_cloud_tab.wait()
    first_cloud_project_cloud_tab = cloud_project_elts.first_cloud_project_cloud_tab.find().text
    logging.info(f"Found first cloud project {first_cloud_project_cloud_tab}")

    assert project_title == first_cloud_project_cloud_tab, \
        "Expected {project_title} to be the first cloud project in {username}'s Cloud tab, " \
        f"but instead got {first_cloud_project_cloud_tab}"

    logging.info(f"Checking if a remote is set for project {project_title}")
    project_path = os.path.join(os.environ['GIGANTUM_HOME'], username, username,
                                'labbooks', project_title)
    git_get_remote_command_1 = Popen(['git', 'remote', 'get-url', 'origin'],
                                     cwd=project_path, stdout=PIPE, stderr=PIPE)
    cloud_project_stdout = git_get_remote_command_1.stdout.readline().decode('utf-8').strip()

    assert "https://" in cloud_project_stdout, f"Expected to see a remote set for project {project_title}, " \
                                               f"but got {cloud_project_stdout}"

    # Add a file and sync cloud project
    driver.get(f'{os.environ["GIGANTUM_HOST"]}/projects/{username}/{project_title}/inputData')
    time.sleep(3)
    file_browser_elts = testutils.FileBrowserElements(driver)
    file_browser_elts.drag_drop_file_in_drop_zone()
    cloud_project_elts.sync_cloud_project(project_title)

    assert "Sync complete" in cloud_project_elts.sync_project_message.find().text, \
        "Expected 'Sync complete' in footer"

    # Delete cloud project
    cloud_project_elts.delete_cloud_project(project_title)

    # Assert project does not exist in cloud tab
    assert project_title != first_cloud_project_cloud_tab, \
        f"Expected {project_title} to not be the first cloud project in {username}'s Cloud tab, " \
        f"but instead got {first_cloud_project_cloud_tab}"

    # Assert project does not exist remotely (via GraphQL)
    remote_projects = graphql.list_remote_projects()

    assert (username, project_title) not in remote_projects

    # Assert that project does not have remote Git repo (use Git 2.20+)
    git_get_remote_command_2 = Popen(['git', 'remote', 'get-url', 'origin'],
                                     cwd=project_path, stdout=PIPE, stderr=PIPE)
    del_cloud_project_stderr = git_get_remote_command_2.stderr.readline().decode('utf-8').strip()

    assert "fatal" in del_cloud_project_stderr, f"Expected to not see a remote set for project {project_title}, " \
                                                f"but got {del_cloud_project_stderr}"


def test_publish_collaborator(driver: selenium.webdriver, *args, ** kwargs):
    """
        Test that a project in Gigantum can be published, shared with a collaborator, and imported by the collaborator.
    """
    # Create and publish project
    r = testutils.prep_py3_minimal_base(driver)
    username, project_title = r.username, r.project_name
    cloud_project_elts = testutils.CloudProjectElements(driver)
    cloud_project_elts.publish_private_project(project_title)
    # Add collaborator
    collaborator = cloud_project_elts.add_collaborator_read_permissions(project_title)
    # Owner logs out
    side_bar_elts = testutils.SideBarElements(driver)
    side_bar_elts.do_logout()

    # Collaborator logs in


    logging.info(f"Logging in as {collaborator}")
    username2 = testutils.load_credentials(user_index=1)[0].rstrip()
    publish_elts.collaborators_input.send_keys(username2)

    testutils.log_in(driver, user_index=1)
    time.sleep(2)
    try:
        testutils.GuideElements.remove_guide(driver)
    except:
        pass
    time.sleep(2)
    publish_elts.cloud_tab.click()
    time.sleep(2)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".RemoteLabbooks__panel-title")))

    # Test that shared cloud project is in cloud tab
    cloud_tab_first_project_title_delete = driver.find_element_by_css_selector(
        ".RemoteLabbooks__panel-title:first-child span span").text
    assert cloud_tab_first_project_title_delete == project_title, \
        f"Expected shared cloud project {project_title} in cloud tab"

    publish_elts.import_first_cloud_project_button.click()
    time.sleep(2)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))

    # Test that after import, the shared project opens to overview page
    shared_project_title = publish_elts.overview_project_title.find().text
    assert project_title in shared_project_title, \
        f"After import, expected shared project {project_title} to open to overview page"

    testutils.log_out(driver)

    # Delete cloud project
    logging.info(f"Logging in as {username}")
    testutils.log_in(driver)
    time.sleep(2)
    try:
        testutils.GuideElements.remove_guide(driver)
    except:
        pass
    time.sleep(2)
    testutils.delete_project_cloud(driver, project_title)

    # Assert project does not exist remotely (Via GraphQL).
    # TODO - Put back in check for the UI in addition to this check.
    remote_projects = graphql.list_remote_projects()
    assert (username, project_title) not in remote_projects

    # Check that the actual Git repo in the project had the remote removed successfully
    # Note! Use Git 2.20+
    logging.info("Testing git remotes to check if set...")
    project_path = os.path.join(os.environ['GIGANTUM_HOME'], username, username,
                                'labbooks', project_title)
    git_get_remote_command_2 = Popen(['git', 'remote', 'get-url', 'origin'],
                                     cwd=project_path, stdout=PIPE, stderr=PIPE)
    del_stderr = git_get_remote_command_2.stderr.readline().decode('utf-8').strip()

    assert "fatal" in del_stderr, f"Expected to not see a remote set for {project_title}, but got {del_stderr}"


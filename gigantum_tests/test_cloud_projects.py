# Builtin imports
import logging
import time
import os
import shutil
from subprocess import Popen, PIPE

# Library imports
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Local packages
import testutils
from testutils import graphql


def test_publish_sync_delete_project(driver: selenium.webdriver, *args, **kwargs):
    """
        Test that a project in Gigantum can be published, synced, and deleted.

        Args:
            driver
    """
    r = testutils.prep_py3_minimal_base(driver)
    username, project_title = r.username, r.project_name

    # Publish project, then wait until its rebuilt
    logging.info(f"Publishing private project {project_title}")
    publish_elts = testutils.PublishProjectElements(driver)
    time.sleep(1)
    publish_elts.publish_project_button.click()
    time.sleep(1)
    publish_elts.publish_confirm_button.click()
    time.sleep(5)
    wait = WebDriverWait(driver, 15)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))
    time.sleep(5)

    # Navigate to cloud tab
    logging.info(f"Navigating to {username}'s' cloud view")
    driver.get(f'{os.environ["GIGANTUM_HOST"]}/projects/cloud')

    sel = 'div[data-selenium-id="RemoteLabbookPanel"]:first-child'
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, sel)))
    time.sleep(2)


    ssel = f'{sel} span'
    cloud_tab_first_project_title_publish = driver.find_element_by_css_selector(ssel).text
    logging.info(f"!!!!! {cloud_tab_first_project_title_publish}")

    assert cloud_tab_first_project_title_publish == project_title, \
        f"Expected {project_title} to be the first project in the cloud tab"


    logging.info("Testing git remotes to check if set...")
    project_path = os.path.join(os.environ['GIGANTUM_HOME'], username, username,
                                'labbooks', project_title)
    git_get_remote_command_1 = Popen(['git', 'remote', 'get-url', 'origin'],
                                     cwd=project_path, stdout=PIPE, stderr=PIPE)
    pub_stdout = git_get_remote_command_1.stdout.readline().decode('utf-8').strip()
    assert "https://" in pub_stdout, f"Expected to see a remote set for private project " \
                                     f"{project_title}, but got {pub_stdout}"

    publish_elts.local_tab.click()
    driver.get(f'{os.environ["GIGANTUM_HOST"]}/projects/{username}/{project_title}')
    time.sleep(3)

    # Add file to input data and sync project
    logging.info("Adding a file to the project")
    with open('/tmp/sample-upload.txt', 'w') as example_file:
        example_file.write('Sample Text')
    input_path = os.path.join(os.environ['GIGANTUM_HOME'], username, username, 'labbooks', project_title,
                              'input')
    shutil.copy(example_file.name, input_path)
    logging.info(f"Syncing {project_title}")
    publish_elts.sync_project_button.click()
    time.sleep(3)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))

    sync_message = driver.find_element_by_css_selector(".Footer__message-item > p").text
    assert "Sync complete" in sync_message, "Expected 'Sync complete' in footer"

    side_bar_elts = testutils.SideBarElements(driver)
    side_bar_elts.projects_icon.click()
    time.sleep(1)
    publish_elts.cloud_tab.click()
    time.sleep(2)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".RemoteLabbooks__panel-title")))

    # Delete cloud project
    logging.info(f"Deleting {project_title} from cloud")
    publish_elts.delete_project_button.click()
    time.sleep(2)
    publish_elts.delete_project_input.send_keys(project_title)
    time.sleep(2)
    publish_elts.delete_confirm_button.click()
    time.sleep(5)

    # Test that the project is not the first project in the cloud tab
    cloud_tab_first_project_title_delete = driver.find_element_by_css_selector(
        ".RemoteLabbooks__panel-title:first-child span span").text
    assert cloud_tab_first_project_title_delete != project_title, \
        f"Expected {project_title} to not be the first project in the cloud tab"

    publish_elts.local_tab.click()
    time.sleep(2)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".LocalLabbooks__panel-title")))

    # Test that the project is the first project in the local tab
    local_tab_first_project_title = driver.find_element_by_css_selector(
        ".LocalLabbooks__panel-title:first-child span span").text
    assert local_tab_first_project_title == project_title, \
        f"Expected {project_title} to be the first project in the local tab"

    git_get_remote_command_2 = Popen(['git', 'remote', 'get-url', 'origin'],
                                     cwd=project_path, stdout=PIPE, stderr=PIPE)
    del_stderr = git_get_remote_command_2.stderr.readline().decode('utf-8').strip()

    assert "fatal" in del_stderr, f"Expected to not see a remote set for {project_title}, but got {del_stderr}"

#
# def test_publish_collaborator(driver: selenium.webdriver, *args, ** kwargs):
#     """
#         Test that a project in Gigantum can be published, shared with a collaborator, and imported by the collaborator.
#
#         Args:
#             driver
#     """
#     # Project set up
#     username = testutils.log_in(driver)
#     time.sleep(2)
#     testutils.remove_guide(driver)
#     time.sleep(2)
#
#     return
#
#     project_title = testutils.create_project_without_base(driver)
#
#     # Python 3 minimal base
#     testutils.add_py3_min_base(driver)
#     wait = WebDriverWait(driver, 200)
#     wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))
#     return
#
#     # Publish project
#     publish_elts = testutils.PublishProjectElements(driver)
#     publish_elts.publish_project_button.click()
#     publish_elts.publish_confirm_button.click()
#     time.sleep(2)
#     wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))
#
#     # Add collaborator
#     logging.info(f"Adding a collaborator to private project {project_title}")
#     publish_elts.collaborators_button.click()
#     time.sleep(2)
#     username2 = testutils.load_credentials(user_index=1)
#     publish_elts.collaborators_input.send_keys(username2)
#     publish_elts.add_collaborators_button.click()
#     time.sleep(2)
#     publish_elts.close_collaborators_button.click()
#     testutils.log_out(driver)
#
#     # Collaborator checks that the project is in the cloud tab and that the project imports successfully
#     logging.info(f"Logging in as {username2[0].rstrip()}")
#     testutils.log_in(driver, user_index=1)
#     time.sleep(2)
#     try:
#         testutils.remove_guide(driver)
#     except:
#         pass
#     time.sleep(2)
#     publish_elts.cloud_tab.click()
#     time.sleep(2)
#     wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".RemoteLabbooks__panel-title")))
#
#     # Test that shared cloud project is in cloud tab
#     cloud_tab_first_project_title_delete = driver.find_element_by_css_selector(
#         ".RemoteLabbooks__panel-title:first-child span span").text
#     assert cloud_tab_first_project_title_delete == project_title, \
#         f"Expected shared cloud project {project_title} in cloud tab"
#
#     publish_elts.import_first_cloud_project_button.click()
#     time.sleep(2)
#     wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))
#
#     # Test that after import, the shared project opens to overview page
#     shared_project_title = driver.find_element_by_css_selector(".TitleSection__namespace-title").text
#     assert project_title in shared_project_title, \
#         f"After import, expected shared project {project_title} to open to overview page"
#
#     testutils.log_out(driver)
#
#     # Owner deletes cloud project
#     testutils.log_in(driver)
#     time.sleep(2)
#     try:
#         testutils.remove_guide(driver)
#     except:
#         pass
#     time.sleep(2)
#     logging.info(f"{username} deleting shared {project_title} from cloud")
#     publish_elts.cloud_tab.click()
#     time.sleep(2)
#     wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".RemoteLabbooks__panel-title")))
#     publish_elts.delete_project_button.click()
#     time.sleep(2)
#     publish_elts.delete_project_input.send_keys(project_title)
#     time.sleep(2)
#     publish_elts.delete_confirm_button.click()
#     time.sleep(5)
#     project_path = os.path.join(os.environ['GIGANTUM_HOME'], username, username,
#                                 'labbooks', project_title)
#     git_get_remote_command_1 = Popen(['git', 'remote', 'get-url', 'origin'],
#                                      cwd=project_path, stdout=PIPE, stderr=PIPE)
#     del_stderr = git_get_remote_command_1.stderr.readline().decode('utf-8').strip()
#
#     assert "fatal" in del_stderr, f"Expected to not see a remote set for {project_title}, but got {del_stderr}"
#
#
#

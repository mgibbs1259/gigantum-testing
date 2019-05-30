import logging

import selenium
from selenium.webdriver.common.by import By

import testutils


def test_featured_public_projects(driver: selenium.webdriver, *args, **kwargs):
    """
    Test that featured public projects import and build successfully.
    """
    # Log in and turn off guide
    login_elts =
    # Import featured public projects
    # TO DO - add in https://gigantum.com/gigantum-examples/allen-sdk-examples
    # TO DO - add in gigantum.com/randal/baltimore-sun-data-bridge-data
    featured_public_projects = ["gigantum.com/meg297/military-expenditure-gdp-population",
                                "gigantum.com/billvb/fsw-telecoms-study"]
    for project in featured_public_projects:
        logging.info(f"Importing featured public project: {project_title}")
        import_project_elts = testutils.ImportProjectElements(driver)
        import_project_elts.import_existing_button.wait().click()
        import_project_elts.project_url_input.wait().send_keys(project_title)
        import_project_elts.import_button.wait().click()
        container_elts = testutils.ContainerElements(driver)
        container_elts.container_status_stopped.wait()
        #wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#overview")))
        #wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))

        assert container_elts.container_status_stopped.find().is_displayed(), "Expected stopped container status"

        logging.info(f"Featured public project {project_title} was imported successfully")
        side_bar_elts = testutils.SideBarElements(driver)
        side_bar_elts.projects_icon.find().click()

# Builtin imports
import logging
import time

# Library imports
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Local packages
import testutils


def test_featured_public_projects(driver: selenium.webdriver, *args, **kwargs):
    """
    Test that featured public projects import and build successfully.

    Args:
        driver
    """
    # Project set up
    testutils.log_in(driver)
    time.sleep(2)
    testutils.remove_guide(driver)
    time.sleep(2)
    # Import featured public projects
    import_project_elts = testutils.ImportProjectElements(driver)
    side_bar_elts = testutils.SideBarElements(driver)
    # TO DO - add in https://gigantum.com/gigantum-examples/allen-sdk-examples
    # TO DO - add in gigantum.com/randal/baltimore-sun-data-bridge-data
    featured_public_projects = ["gigantum.com/meg297/military-expenditure-gdp-population",
                                "gigantum.com/billvb/fsw-telecoms-study"]
    for project in featured_public_projects:
        logging.info(f"Importing featured public project: {project}")
        import_project_elts.import_existing_button.click()
        time.sleep(2)
        import_project_elts.project_url_input.send_keys(project)
        time.sleep(2)
        import_project_elts.import_button.click()
        wait = selenium.webdriver.support.ui.WebDriverWait(driver, 200)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#overview")))
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))

        project_stopped_visible = driver.find_element_by_css_selector(".flex>.Stopped").is_displayed()
        assert project_stopped_visible, "Expected stopped container status"

        logging.info(f"Featured public project {project} was imported successfully")
        side_bar_elts.side_bar_projects_icon.click()
        time.sleep(2)
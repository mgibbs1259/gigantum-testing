# Builtin imports
import time

# Library imports
import selenium
from selenium.webdriver.common.by import By

# Local packages
import testutils


def test_featured_public_projects(driver: selenium.webdriver, *args, **kwargs):
    """
    Test that featured public projects import and build successfully.

    Args:
        driver
    """
    # Log in and remove guide
    testutils.log_in_remove_guide(driver)
    # Import featured public projects
    # TODO - add gigantum.com/gigantum-examples/allen-sdk-examples
    # TODO - add gigantum.com/randal/baltimore-sun-data-bridge-data
    testutils.import_project_via_project_link(driver, "gigantum.com/meg297/military-expenditure-gdp-population")

    project_stopped_visible = driver.find_element_by_css_selector(".flex>.Stopped").is_displayed()
    assert project_stopped_visible, "Expected stopped container status"

    side_bar_elts = testutils.SideBarElements(driver)
    side_bar_elts.projects_icon.click()
    time.sleep(2)
    testutils.import_project_via_project_link(driver, "gigantum.com/billvb/fsw-telecoms-study")

    project_stopped_visible = driver.find_element_by_css_selector(".flex>.Stopped").is_displayed()
    assert project_stopped_visible, "Expected stopped container status"





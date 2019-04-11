# Builtin imports
import logging
import time

# Library imports
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Local packages
import testutils


def test_pip_packages(driver: selenium.webdriver, *args, **kwargs):
    """
    Test that pip packages install successfully.

    Args:
        driver
    """
    # Create project
    testutils.log_in_remove_guide(driver)
    testutils.create_project_without_base(driver)
    testutils.add_py3_min_base(driver)
    # Add pip packages
    testutils.add_pip_package(driver)
    # Get environment package versions
    logging.info("Getting package versions from environment")
    env_elts = testutils.EnvironmentElements(driver)
    environment_package_table = env_elts.package_info_table.text
    environment_package_text = environment_package_table.split("\n")[1::3]
    environment_package_parse = [x.split(" ") for x in environment_package_text]
    environment_package_versions = {x[0]: x[1] for x in environment_package_parse if len(x) > 1}
    # Open JupyterLab
    testutils.create_jupyter_notebook(driver)
    logging.info("Running script to import packages and print package versions")
    actions = ActionChains(driver)
    jupyterlab_elts = testutils.JupyterLabElements(driver)
    package_script = "import pandas\nimport numpy\nimport matplotlib\n" \
                     "print('pandas', pandas.__version__," \
                     " 'numpy',numpy.__version__," \
                     " 'matplotlib', matplotlib.__version__)"
    actions.move_to_element(jupyterlab_elts.code_input)
    actions.click(jupyterlab_elts.code_input).send_keys(package_script).perform()
    jupyterlab_elts.run_button.click()
    time.sleep(3)
    # Get JupyterLab package versions
    logging.info("Getting package versions from JupyterLab")
    package_output = driver.find_element_by_css_selector(".jp-OutputArea-output > pre").text.split(" ")
    # convert to dictionary with package names as key and versions as values.
    package_jupyter = dict(zip(package_output[::2], package_output[1::2]))
    logging.info("Getting package versions from jupyterlab")
    # check if package versions from environment and from jupyter notebook are same.
    logging.info(f"package_environment {package_environment} \n package_jupyter {package_jupyter}")

    assert environment_package_versions == jupyterlab_package_versions, "Environment and JupyterLab package " \
                                                                        "versions do not match"


def test_valid_custom_docker(driver: selenium.webdriver, *args, **kwargs):
    """
    Test valid custom Docker instructions.

    Args:
        driver
    """
    # project set up
    testutils.log_in(driver)
    time.sleep(2)
    testutils.remove_guide(driver)
    testutils.create_project_without_base(driver)
    time.sleep(2)
    # python 2 minimal base
    testutils.add_py3_min_base(driver)
    # wait until container status is stopped
    wait = selenium.webdriver.support.ui.WebDriverWait(driver, 200)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))
    # add a valid custom docker instruction
    testutils.add_valid_custom_docker(driver)
    # wait until container status is stopped
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))
    # assert container status is stopped and 'Successfully tagged' is in footer
    assert driver.find_element_by_css_selector(".flex>.Stopped").is_displayed(), "Expected stopped container"
    assert "Successfully tagged" in driver.find_element_by_css_selector(".Footer__message-title").text, "Expected 'Successfully tagged' in footer"


def test_invalid_custom_docker(driver: selenium.webdriver, *args, **kwargs):
    """
    Test invalid custom Docker instructions.

    Args:
        driver
    """
    # project set up
    testutils.log_in(driver)
    time.sleep(2)
    testutils.remove_guide(driver)
    testutils.create_project_without_base(driver)
    time.sleep(2)
    # python 2 minimal base
    testutils.add_py3_min_base(driver)
    # wait until container status is stopped
    wait = selenium.webdriver.support.ui.WebDriverWait(driver, 200)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))
    # add an invalid custom docker instruction
    testutils.add_invalid_custom_docker(driver)
    # wait until container status is stopped
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Rebuild")))
    time.sleep(2)
    # assert container status is stopped and 'Successfully tagged' is in footer
    assert driver.find_element_by_css_selector(".flex>.Rebuild").is_displayed(), "Expected rebuild container status"
    assert "Project failed to build" in driver.find_element_by_css_selector(".Footer__message-title").text, "Expected 'Project failed to build' in footer"


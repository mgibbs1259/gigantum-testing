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
    r = testutils.prep_py3_minimal_base(driver)
    username, project_title = r.username, r.project_name
    # Add pip packages
    env_elts = testutils.EnvironmentElements(driver)
    env_elts.add_pip_package()
    time.sleep(3)
    # Get environment package versions
    logging.info("Getting package versions from environment")
    environment_package_table = env_elts.package_info_table.text
    environment_package_text = environment_package_table.split("\n")[1::3]
    environment_package_parse = [x.split(" ") for x in environment_package_text]
    environment_package_versions = {x[0]: x[1] for x in environment_package_parse if len(x) > 1}
    # Open JupyterLab and create Jupyter notebook
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
    jupyterlab_package_output = jupyterlab_elts.code_output.text.split(" ")
    jupyterlab_package_versions = dict(zip(jupyterlab_package_output[::2], jupyterlab_package_output[1::2]))

    assert environment_package_versions == jupyterlab_package_versions,\
        "Environment and JupyterLab package versions do not match"


def test_valid_custom_docker(driver: selenium.webdriver, *args, **kwargs):
    """
    Test valid custom Docker instructions.

    Args:
        driver
    """
    # Create project
    r = testutils.prep_py3_minimal_base(driver)
    username, project_title = r.username, r.project_name
    # Add a valid custom docker instruction
    testutils.add_custom_docker_instructions(driver, testutils.valid_custom_docker_instruction())
    time.sleep(5)
    wait = WebDriverWait(driver, 200)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))
    time.sleep(3)

    container_status = driver.find_element_by_css_selector(".flex>.Stopped").is_displayed()
    assert container_status, "Expected stopped container status"


def test_invalid_custom_docker(driver: selenium.webdriver, *args, **kwargs):
    """
    Test invalid custom Docker instructions.

    Args:
        driver
    """
    # Create project
    r = testutils.prep_py3_minimal_base(driver)
    username, project_title = r.username, r.project_name
    # Add an invalid custom docker instruction
    testutils.add_custom_docker_instructions(driver, testutils.invalid_custom_docker_instruction())
    time.sleep(5)
    wait = WebDriverWait(driver, 200)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Rebuild")))
    time.sleep(3)

    container_status = driver.find_element_by_css_selector(".flex>.Rebuild").is_displayed()
    assert container_status, "Expected rebuild container status"

    footer_message_text = driver.find_element_by_css_selector(".Footer__message-title").text
    assert "Project failed to build" in footer_message_text, "Expected 'Project failed to build' in footer message"



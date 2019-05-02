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
    return
    # project set up
    r = testutils.prep_py3_minimal_base(driver)
    username, project_name = r.username, r.project_name

    testutils.add_pip_package(driver)
    time.sleep(5)
    # wait until container status is stopped
    wait = selenium.webdriver.support.ui.WebDriverWait(driver, 30)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex > .Stopped")))
    assert testutils.is_container_stopped(driver), "Expected stopped container"

    # check package versions from environment
    package_info = driver.find_element_by_css_selector(".PackageDependencies__table").text
    # parse the string to a list and extract information of package names and versions
    package_list = package_info.split("\n")[1::3]
    package_parse = [x.split(" ") for x in package_list]
    # convert to dictionary with package names as key and versions as values
    package_environment = {x[0]: x[1] for x in package_parse if len(x) > 1}
    logging.info("Getting package versions from environment")

    # check pip packages version from jupyterlab
    driver.find_element_by_css_selector(".Btn--text").click()
    time.sleep(10)
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[1])
    logging.info("Switching to jupyter lab")
    # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[title = code]")))
    time.sleep(3)
    driver.find_element_by_css_selector(".jp-LauncherCard-label").click()
    logging.info("Launching jupyter notebook")
    # wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".CodeMirror-line")))
    time.sleep(3)
    el = driver.find_element_by_css_selector(".CodeMirror-line")
    actions = ActionChains(driver)
    logging.info("Importing packages")
    # implement script the import packages and print the versions.
    package_script = "import pandas\nimport numpy\nimport matplotlib\n" \
                     "print('pandas', pandas.__version__," \
                     " 'numpy',numpy.__version__," \
                     " 'matplotlib', matplotlib.__version__)"
    actions.move_to_element(el).click(el).send_keys(package_script).perform()
    driver.find_element_by_css_selector(".jp-RunIcon").click()
    # extract the output of package versions as string and parse to a list.
    logging.info("Extracting package versions from jupyter")
    # wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".jp-mod-active")))
    time.sleep(3)
    package_output = driver.find_element_by_css_selector(".jp-OutputArea-output > pre").text.split(" ")
    # convert to dictionary with package names as key and versions as values.
    package_jupyter = dict(zip(package_output[::2], package_output[1::2]))
    logging.info("Getting package versions from jupyterlab")
    # check if package versions from environment and from jupyter notebook are same.
    logging.info(f"package_environment {package_environment} \n package_jupyter {package_jupyter}")
    assert package_environment == package_jupyter, "Package versions do not match"


    '''
    # stop the container after the test is finished
    driver.switch_to.window(window_handles[0])
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex > .Running")))
    testutils.stop_container(driver)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex > .Stopped")))
    assert testutils.is_container_stopped(driver), "Expected stopped container"

    # conda3 package
    test_project.conda3_package()
    # wait 
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))
    assert driver.find_element_by_css_selector(".flex>.Stopped").is_displayed(), "Expected stopped container"

    # apt package
    test_project.apt_package()
    # wait 
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))
    assert driver.find_element_by_css_selector(".flex>.Stopped").is_displayed(), "Expected stopped container"
    '''


def test_valid_custom_docker(driver: selenium.webdriver, *args, **kwargs):
    """
    Test valid custom Docker instructions.

    Args:
        driver
    """
    r = testutils.prep_py3_minimal_base(driver)
    username, project_name = r.username, r.project_name
    wait = selenium.webdriver.support.ui.WebDriverWait(driver, 200)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))
    logging.info("Adding valid custom Docker")
    environment = testutils.EnvironmentElements(driver)
    environment.environment_tab_button.click()
    driver.execute_script("window.scrollBy(0, 600);")
    environment.custom_docker_edit_button.click()
    environment.custom_docker_text_input.send_keys("RUN cd /tmp && "
                                                   "git clone https://github.com/gigantum/confhttpproxy && "
                                                   "cd /tmp/confhttpproxy && pip install -e.")
    time.sleep(1)
    driver.execute_script("window.scrollBy(0, 300);")
    environment.custom_docker_save_button.click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))
    # assert container status is stopped and 'Successfully tagged' is in footer
    time.sleep(15)
    assert driver.find_element_by_css_selector(".flex>.Stopped").is_displayed(), "Expected stopped container"


def test_invalid_custom_docker(driver: selenium.webdriver, *args, **kwargs):
    """
    Test invalid custom Docker instructions.

    Args:
        driver
    """
    r = testutils.prep_py3_minimal_base(driver)
    username, project_name = r.username, r.project_name
    # add an invalid custom docker instruction
    logging.info("Adding invalid custom Docker")
    environment = testutils.EnvironmentElements(driver)
    environment.environment_tab_button.click()
    time.sleep(1)
    driver.execute_script("window.scrollBy(0, 600);")
    environment.custom_docker_edit_button.click()
    time.sleep(1)
    environment.custom_docker_text_input.send_keys("RUN /bin/false")
    time.sleep(1)
    driver.execute_script("window.scrollBy(0, 300);")
    environment.custom_docker_save_button.click()
    # wait until container status is stopped
    wait = selenium.webdriver.support.ui.WebDriverWait(driver, 200)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Rebuild")))
    time.sleep(2)
    # assert container status is stopped and 'Successfully tagged' is in footer
    envelts = testutils.elements.EnvironmentElements(driver)
    assert driver.find_element_by_css_selector(".flex>.Rebuild").is_displayed(), "Expected rebuild container status"
    assert "Project failed to build" in driver.find_element_by_css_selector(".Footer__message-title").text, \
        "Expected 'Project failed to build' in footer"

# Builtin imports
import logging
import time

# Library imports
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Local packages
from testutils import elements
from testutils import testutils


def log_in_remove_guide(driver: selenium.webdriver, user_index: int = 0) -> str:
    """
    Log in to Gigantum and remove 'Got it!', guide, and helper.

    Args:
        driver
        user_index: An offset into credentials.txt.

    Returns:
        Username of user that logged in.
    """
    driver.get("http://localhost:10000/projects/local#")
    login_elts = elements.LoginElements(driver)
    login_elts.login_green_button.click()
    time.sleep(2)
    try:
        if login_elts.auth0_lock_button:
            logging.info("Clicking 'Not your account?'")
            login_elts.not_your_account_button.click()
    except:
        pass
    username, password = testutils.load_credentials(user_index=user_index)
    logging.info(f"Logging in as {username}")
    login_elts.username_input.click()
    login_elts.username_input.send_keys(username)
    login_elts.password_input.click()
    login_elts.password_input.send_keys(password)
    try:
        login_elts.login_grey_button.click()
    except:
        pass
    time.sleep(2)
    logging.info("Getting rid of 'Got it!'")
    guide_elts = elements.GuideElements(driver)
    guide_elts.got_it_button.click()
    logging.info("Turning off guide and helper")
    guide_elts.guide_button.click()
    guide_elts.helper_button.click()

    return username.strip()


def import_project_via_project_link(driver: selenium.webdriver, project_link):
    """
    Import a project via project link.

    Args:
        driver
        project_link (str): Link of project to be imported.
    """
    logging.info(f"Importing featured public project: {project_link}")
    import_project_elts = elements.ImportProjectElements(driver)
    import_project_elts.import_existing_button.click()
    time.sleep(2)
    import_project_elts.project_url_input.send_keys(project_link)
    time.sleep(2)
    import_project_elts.import_button.click()
    wait = selenium.webdriver.support.ui.WebDriverWait(driver, 200)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#overview")))
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))
    logging.info(f"Featured public project {project_link} was imported successfully")


def create_project_without_base(driver: selenium.webdriver) -> str:
    """
    Create a project without a base.

    Args:
        driver
    
    Returns:
        Name of project that was created.
    """
    unique_project_name = testutils.unique_project_name()
    logging.info(f"Creating a new project: {unique_project_name}")
    project_elts = elements.AddProjectElements(driver)
    project_elts.create_new_button.click()
    project_elts.project_title_input.click()
    project_elts.project_title_input.send_keys(unique_project_name)
    project_elts.project_description_input.click()
    project_elts.project_description_input.send_keys(testutils.unique_project_description())
    project_elts.project_continue_button.click()

    return unique_project_name


def add_py2_min_base(driver: selenium.webdriver):
    """
    Add a Python2 Minimal base.

    Args:
        driver
    """
    logging.info("Creating new project with Python2 Minimal base")
    py2_base_elts = elements.AddProjectBaseElements(driver)
    try:
        py2_base_elts.py2_tab_button.click()
    except:
        pass
    while not py2_base_elts.py2_minimal_base_button.is_displayed():
        logging.info("Searching for Python2 Minimal base...")
        py2_base_elts.arrow_button.click()
    py2_base_elts.py2_minimal_base_button.click()
    py2_base_elts.create_project_button.click()


def add_py3_min_base(driver: selenium.webdriver):
    """
    Add a Python3 Minimal base.

    Args:
        driver
    """
    logging.info("Creating new project with Python3 Minimal base")
    py3_base_elts = elements.AddProjectBaseElements(driver)
    try:
        py3_base_elts.py3_tab_button.click()
    except:
        pass
    while not py3_base_elts.py3_minimal_base_button.is_displayed():
        logging.info("Searching for Python3 Minimal base...")
        py3_base_elts.arrow_button.click()
    py3_base_elts.py3_minimal_base_button.click()
    py3_base_elts.create_project_button.click()
    wait = WebDriverWait(driver, 200)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))


def add_py3_ds_base(driver: selenium.webdriver):
    """
    Add a Python3 Data Science Quick-start base.

    Args:
        driver
    """
    logging.info("Creating new project with Python3 Data Science Quick-start base")
    py3_base_elts = elements.AddProjectBaseElements(driver)
    try:
        py3_base_elts.py3_tab_button.click()
    except:
        pass
    while not py3_base_elts.py3_minimal_base_button.is_displayed():
        logging.info("Searching for Python3 Data Science Quick-start base...")
        py3_base_elts.arrow_button.click()
    py3_base_elts.py3_data_science_base_button.click()
    py3_base_elts.create_project_button.click()


def add_rtidy_base(driver: selenium.webdriver):
    """
    Add a R Tidyverse base.

    Args:
        driver
    """
    logging.info("Creating new project with R Tidyverse base")
    r_base_elts = elements.AddProjectBaseElements(driver)
    try:
        r_base_elts.r_tab_button.click()
    except:
        pass
    while not r_base_elts.r_tidyverse_base_button.is_displayed():
        logging.info("Searching for R Tidyverse base...")
        r_base_elts.arrow_button.click()
    r_base_elts.r_tidyverse_base_button.click()
    r_base_elts.create_project_button.click()


def add_pip_package(driver: selenium.webdriver):
    """
    Add pip packages.

    Args:
        driver
    """
    logging.info("Adding pip packages")
    environment = elements.EnvironmentElements(driver)
    environment.environment_tab_button.click()
    time.sleep(2)
    driver.execute_script("window.scrollBy(0, -400);")
    driver.execute_script("window.scrollBy(0, 400);")
    environment.add_packages_button.click()
    pip_list = ["pandas", "numpy", "matplotlib"]
    for pip_pack in pip_list:
        environment.package_name_input.send_keys(pip_pack)
        time.sleep(2)
        environment.add_button.click()
        time.sleep(2)
    environment.install_packages_button.click()
    time.sleep(5)
    wait = WebDriverWait(driver, 200)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))


def add_conda3_package(driver: selenium.webdriver):
    """
    Add conda3 packages.

    Args:
        driver
    """
    logging.info("Adding conda3 package")
    environment = elements.EnvironmentElements(driver)
    environment.environment_tab_button.click()
    time.sleep(3)
    environment.conda3_tab_button.click()
    driver.execute_script("window.scrollBy(0, -400);")
    driver.execute_script("window.scrollBy(0, 400);")
    environment.add_packages_button.click()
    environment.package_name_input.send_keys("pyflakes")
    time.sleep(3)
    environment.add_button.click()
    time.sleep(3)
    environment.install_packages_button.click()


def add_apt_package(driver: selenium.webdriver):
    """
    Add apt packages.

    Args:
        driver
    """
    logging.info("Adding apt packages")
    environment = elements.EnvironmentElements(driver)
    environment.environment_tab_button.click()
    time.sleep(3)
    environment.apt_tab_button.click()
    driver.execute_script("window.scrollBy(0, -400);")
    driver.execute_script("window.scrollBy(0, 400);")
    environment.add_packages_button.click()
    environment.package_name_input.send_keys("apache2")
    time.sleep(3)
    environment.add_button.click()
    time.sleep(3)
    environment.install_packages_button.click()


def add_custom_docker_instructions(driver: selenium.webdriver, docker_instruction):
    """
    Add custom Docker instructions.

    Args:
        driver
        docker_instruction (str): Docker instruction from testutils.py.
    """
    logging.info("Adding custom Docker instruction")
    environment = elements.EnvironmentElements(driver)
    environment.environment_tab_button.click()
    driver.execute_script("window.scrollBy(0, 600);")
    environment.custom_docker_edit_button.click()
    environment.custom_docker_text_input.send_keys(docker_instruction)
    driver.execute_script("window.scrollBy(0, 300);")
    environment.custom_docker_save_button.click()


def delete_project(driver: selenium.webdriver, project_name):
    """
    Delete a project.

    Args:
        driver
        project_name (str): Name of project to be deleted.
    """
    logging.info("Navigating to 'Delete Project'")
    del_proj_elts = elements.DeleteProjectElements(driver)
    del_proj_elts.actions_button.click()
    time.sleep(2)
    logging.info(f"Deleting project {project_name}")
    del_proj_elts.actions_delete_button.click()
    time.sleep(2)
    del_proj_elts.delete_text_input.send_keys(project_name)
    del_proj_elts.delete_project_button.click()
    time.sleep(5)


def create_jupyter_notebook(driver: selenium.webdriver):
    """
    Open JupyterLab.

    Args:
        driver
    """
    logging.info("Switching to JupyterLab")
    jupyterlab_elts = elements.JupyterLabElements(driver)
    jupyterlab_elts.jupyterlab_button.click()
    time.sleep(10)
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[1])
    time.sleep(5)
    jupyterlab_elts.jupyter_notebook_button.click()
    time.sleep(5)


def create_dataset(driver: selenium.webdriver) -> str:
    """
    Create a dataset.

    Args:
        driver

    Returns:
        Name of dataset just created
    """
    unique_dataset_name = testutils.unique_dataset_name()
    logging.info(f"Creating a new dataset: {unique_dataset_name}")
    dataset_elts = elements.AddDatasetElements(driver)
    dataset_elts.dataset_page_tab.click()
    dataset_elts.create_new_button.click()
    dataset_elts.dataset_title_input.click()
    dataset_elts.dataset_title_input.send_keys(unique_dataset_name)
    dataset_elts.dataset_description_input.click()
    dataset_elts.dataset_description_input.send_keys(testutils.unique_project_description())
    dataset_elts.dataset_continue_button.click()
    dataset_elts.gigantum_cloud_button.click()
    dataset_elts.create_dataset_button.click()
    wait = WebDriverWait(driver, 200)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".TitleSection")))
    return unique_dataset_name


def publish_dataset(driver: selenium.webdriver):
    """
    Publish a dataset to cloud.

    Args:
        driver
    """
    logging.info("Publish dataset to cloud")
    dataset_elts = elements.AddDatasetElements(driver)
    dataset_elts.publish_dataset_button.click()
    dataset_elts.publish_confirm_button.click()
    time.sleep(5)
    dataset_elts.dataset_page_tab.click()
    time.sleep(5)
    dataset_elts.dataset_cloud_page.click()
    wait = WebDriverWait(driver, 200)
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".VisibilityModal__buttons")))


def log_out(driver: selenium.webdriver):
    """
    Log out of Gigantum.

    Args:
     driver
    """
    logging.info("Logging out")
    time.sleep(2)
    side_bar_elts = elements.SideBarElements(driver)
    side_bar_elts.username_button.click()
    time.sleep(2)
    side_bar_elts.logout_button.click()
    time.sleep(2)


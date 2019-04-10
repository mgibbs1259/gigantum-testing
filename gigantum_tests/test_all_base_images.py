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


logging.basicConfig(level=logging.INFO)


def run_base(driver: selenium.webdriver, add_base):
    """
    Create a project with a specified base.

    Args:
        driver
        add_base_image: add base image method from actions.py
    """
    # Project set up
    testutils.log_in(driver)
    time.sleep(2)
    testutils.remove_guide(driver)
    testutils.create_project_without_base(driver)
    time.sleep(4)
    # Add base
    add_base(driver)
    # Wait until container is stopped
    wait = selenium.webdriver.support.ui.WebDriverWait(driver, 200)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex>.Stopped")))
    # Assert container is stopped
    container_elts = testutils.ContainerStatus(driver)
    assert container_elts.container_status_stop.is_displayed(), "Expected stopped container"


def test_py2_min_base(driver: selenium.webdriver, *args, **kwargs):
    """
    Test the creation of a project with a python 2 minimal base.

    Args:
        driver
    """
    run_base(driver, testutils.add_py2_min_base)



def test_py3_min_base(driver: selenium.webdriver, *args, **kwargs):
    """
    Test the creation a project with a python 3 minimal base.

    Args:
        driver
    """
    run_base(driver, testutils.add_py3_min_base)


def test_py3_ds_base(driver: selenium.webdriver, *args, **kwargs):
    """
    Test the creation of a project with a python 3 data science base.

    Args:
        driver
    """
    run_base(driver, testutils.add_py3_ds_base)


def test_rtidy_base(driver: selenium.webdriver, *args, **kwargs):
    """
    Test the creation of a project with a R Tidyverse base.

    Args:
        driver
    """
    run_base(driver, testutils.add_rtidy_base)


def test_py3_min_cuda_10_base(driver: selenium.webdriver, *args, **kwargs):
    """
    Test the creation a project with a python 3 minimal CUDA 10.0 base.

    Args:
        driver
    """
    run_base(driver, testutils.add_py3_min_cuda_10_base)


def test_py3_min_cuda_8_base(driver: selenium.webdriver, *args, **kwargs):
    """
    Test the creation a project with a python 3 minimal CUDA 8.0 base.

    Args:
        driver
    """
    run_base(driver, testutils.add_py3_min_cuda_8_base)


def test_py3_min_cuda_90_base(driver: selenium.webdriver, *args, **kwargs):
    """
    Test the creation a project with a python 3 minimal CUDA 9.0 base.

    Args:
        driver
    """
    run_base(driver, testutils.add_py3_min_cuda_90_base)


def test_py3_min_cuda_91_base(driver: selenium.webdriver, *args, **kwargs):
    """
    Test the creation a project with a python 3 minimal CUDA 9.1 base.

    Args:
        driver
    """
    run_base(driver, testutils.add_py3_min_cuda_91_base)


def test_py3_min_cuda_92_base(driver: selenium.webdriver, *args, **kwargs):
    """
    Test the creation a project with a python 3 minimal CUDA 9.2 base.

    Args:
        driver
    """
    run_base(driver, testutils.add_py3_min_cuda_92_base)


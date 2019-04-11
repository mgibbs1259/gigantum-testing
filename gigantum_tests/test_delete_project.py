# Builtin imports
import logging
import os

# Library imports
import docker
import selenium
from selenium.webdriver.common.by import By

# Local packages
import testutils


def test_delete_project(driver: selenium.webdriver, *args, **kwargs):
    """
        Test that deleting a project in Gigantum deletes it from the
        file system and deletes its Docker image.

        Args:
            driver
    """
    # Create project
    username = testutils.log_in_remove_guide(driver)
    project_name = testutils.create_project_without_base(driver)
    testutils.add_py3_min_base(driver)
    # Find project path on file system
    logging.info(f"Checking project {project_name} exists on file system")
    project_path = os.path.join(os.environ['GIGANTUM_HOME'], username,
                                username, 'labbooks', project_name)

    assert os.path.exists(project_path), f"Project {project_name} should exist at {project_path}"

    # Find project Docker image
    logging.info(f"Finding project {project_name} Docker image")
    dc = docker.from_env()
    project_img = []
    for img in dc.images.list():
        for t in img.tags:
            if 'gmlb-' in t and project_name in t:
                logging.info(f"Found Docker image {t} for project {project_name}")
                project_img.append(img)

    assert len(project_img) == 1, f"Must be one docker tag for project {project_name}"

    # Delete project
    testutils.delete_project(driver, project_name)
    # Check all post conditions for delete:
    # 1. Does not exist in filesystem, and
    # 2. Docker image no longer exists
    logging.info(f"Checking that project {project_name} project path and Docker image no longer exist")

    assert not os.path.exists(project_path), f"Project {project_name} at {project_path} not deleted"

    project_img = []
    for img in dc.images.list():
        for t in img.tags:
            if 'gmlb-' in t and project_name in t:
                logging.error(f"Docker tag {t} still exists for deleted project {project_name}")
                project_img.append(img)

    assert len(project_img) == 0, f"Docker image for {project_path}: {project_img[0]} still exists"



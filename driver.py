#!/usr/bin/env python3
import argparse
import logging
import os

import testutils
from testutils import driverutil


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--headless', default=False, action='store_true',
                           help='Optional name of specific playbook')
    argparser.add_argument('--firefox', default=False, action='store_true',
                           help='Run using Firefox driver (Chrome default)')
    argparser.add_argument('test_path', nargs='?', type=str, default="",
                           help='Optional name of specific playbook')
    args = argparser.parse_args()

    gigantum_home_dir = os.path.expanduser('~/gigantum/')
    os.environ['GIGANTUM_HOME'] = gigantum_home_dir

    if args.firefox:
        driver_loader = testutils.load_firefox_driver
    elif args.headless:
        driver_loader = testutils.load_chrome_driver_headless
    else:
        driver_loader = testutils.load_chrome_driver

    with driverutil.TestRunner() as runner:
        playbooks = driverutil.load_playbooks(os.getcwd(), args.test_path)
        for playbook in playbooks:
            for test_method in playbook.test_methods:
                driver = driver_loader()
                runner.execute_test(test_method, driver)

    runner.render_results()


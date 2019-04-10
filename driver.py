#!/usr/bin/env python3

import datetime
import argparse
import platform
import logging
import time
import json
import sys
import os
import docker

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import boto3

import testutils

TEST_ROOT = os.path.join(os.getcwd(), 'gigantum_tests')
sys.path.append(TEST_ROOT)


def get_playbooks(path):
    # If given a specific path
    if path and 'test_' in path:
        return [path]
    # Else, get all test playbooks, but skip examples
    return [t for t in os.listdir(os.path.join(TEST_ROOT, path))
            if '.py' in t and 'test_' in t and 'test_examples.py' != t]


def load_test_methods(path):
    playbook = __import__(path.replace('.py', ''))
    test_methods = [getattr(playbook, field) for field in dir(playbook)
                    if callable(getattr(playbook, field))
                    and 'test_' in field]
    return test_methods


def save_screenshot(driver, test_func, fail_type, message):
    screenshot_fname = f'{test_func.__name__}--{fail_type}.png'
    screenshot_fname = f'{artifact_dir}/{screenshot_fname}'
    driver.save_screenshot(screenshot_fname)

    img = Image.open(screenshot_fname)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('Arial.ttf', 34)
    draw.text((100, 400), f'{fail_type}: {message}', font=font, fill=(255, 0, 0, 200))
    img.save(screenshot_fname)
    logging.info(f"Wrote screenshot to {screenshot_fname}")


def render_log(test_name, failure_type):
    logfile_path = os.path.join(os.environ['GIGANTUM_HOME'], 
            '.labmanager', 'logs', 'labmanager.log')
    lines = open(logfile_path).readlines()[:15]
    parsed_lines = []
    for l in lines:
        d = json.loads(l)
        # Do not show log messages older than 10 minutes
        if time.time() - d['created'] > 600:
            continue
        parsed_lines.append(f"{d.get('levelname')} -- {d.get('filename')}::"
                            f"{d.get('funcName')}.{d.get('lineno')} -- "
                            f"{d.get('message')}")
    with open(os.path.join(artifact_dir, f"{test_name}.{failure_type}.log"), 'w') as lf:
        lf.write('\n'.join(parsed_lines))


def run_playbook(path, headless, firefox):
    test_methods = load_test_methods(path)
    test_collect = {t.__name__: None for t in test_methods}

    if headless and firefox:
        logging.error('Cannot run firefox in headless mode!')
        sys.exit(1)
   
    for t in test_methods:
        logging.info(f'Running {path}:{t.__name__} ...')
        if firefox:
            driver = testutils.load_firefox_driver()
        elif headless:
            driver = testutils.load_chrome_driver_headless()
        else:
            driver = testutils.load_chrome_driver()

        driver.implicitly_wait(5)
        driver.set_window_size(1440, 1000)
        try:
            t0 = time.time()
            t(driver)
            tfin = time.time()
            logging.info(f'PASS -- {path}:{t.__name__} after {tfin-t0:.2f}s')
            test_collect[t.__name__] = {
                'status': 'PASS',
                'failure_message': None,
                'duration': round(tfin-t0, 2),
                'exception': None
            }
        except Exception as e:
            tfin = time.time()
            fail_type = 'ERROR' if type(e) != AssertionError else 'FAIL'
            logging.error(f'{fail_type} -- {path}:{t.__name__} after {tfin-t0:.2f}s: {e}')
            test_collect[t.__name__] = {
                'status': fail_type,
                'failure_message': str(e),
                'duration': round(tfin-t0),
                'exception': str(type(e))
            }
            save_screenshot(driver, t, fail_type, str(e))
            render_log(t.__name__, fail_type)
        finally:
            driver.quit()
            stop_project_containers(docker_client)
            logging.info("Cleaning up...")
            testutils.cleanup()
            time.sleep(1)

    return test_collect


def stop_project_containers(client):
    containers = client.containers.list()
    for c in containers:
        for t in [c.image.tags]:
            if 'gmlb-' in t:
                logging.info(f"Stopping container for image {t}")
                c.stop()
    logging.info("Pruning all Docker containers")
    logging.info(client.containers.prune())


def upload_to_s3():
    s3client = boto3.resource('s3')
    bucket = s3client.Bucket(os.environ['S3_BUCKET_NAME'])
    
    name = artifact_dir.split('/')[-1]
    for artifact in os.listdir(artifact_dir):
        logging.info(f"Uploading file {artifact}")
        bucket.upload_file(os.path.join(artifact_dir, artifact), 
                           os.path.join(name, artifact))

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


    timestamp = datetime.datetime.utcnow().strftime('%Y%m%d-%H%M')
    artifact_dir = f'/tmp/g-{timestamp}'
    os.makedirs(artifact_dir, exist_ok=True)

    os.environ['GIGANTUM_HOME'] = os.path.expanduser('~/gigantum/')
    docker_client = docker.from_env()
    playbooks = get_playbooks(args.test_path)


    failed = False
    full_results = {
        '_system': {
            'platform': platform.platform(),
            'processor': platform.processor(),
            'os': platform.system(),
            'version': platform.version()
        }
    }
    for pb in playbooks:
        r = run_playbook(pb, args.headless, args.firefox)
        if any([r[l]['status'].lower() != 'pass' for l in r]):
            failed = True
        full_results[pb] = r
        stop_project_containers(docker_client)
    
    logging.info("Cleaning up...")
    testutils.cleanup()

    with open(os.path.join(artifact_dir, 'results.json'), 'w') as result_f:
        result_f.write(json.dumps(full_results, indent=2))

    logging.info(f"Wrote results to {result_f.name}")
    print(f'\n\nTEST SUMMARY ({len(full_results)} tests)\n')
    for test_file in [f for f in full_results.keys() if f[0] != '_']:
        for test_method in full_results[test_file].keys():
            d = full_results[test_file][test_method]
            print(f"{d['status'].upper():6s} :: {test_file}@{test_method} ({d['duration']:.2f} sec) : {d['failure_message'] or ''}")


    if failed:
        try:
            upload_to_s3()
        except:
            logging.info("Skipped uploading to S3")
        sys.exit(1)
    else:
        sys.exit(0)


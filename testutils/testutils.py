# Builtin imports
import subprocess
import logging
import shutil
import time
import uuid
import glob
import uuid
import sys
import os

# Library imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def load_chrome_driver():
    """ Return Chrome webdriver """
    options = Options()
    options.add_argument("--incognito")
    return webdriver.Chrome(options=options)


def load_chrome_driver_headless():
    """ Return headless Chrome webdriver """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--incognito")
    return webdriver.Chrome(options=options)

def load_firefox_driver():
    """ Return Firefox webdriver """
    return webdriver.Firefox()


def unique_project_name(prefix: str = "selenium-project"):
    """ Return a universally-unique project name """
    return f'{prefix}-{uuid.uuid4().hex[:8]}'


def unique_dataset_name(prefix: str = "selenium-dataset"):
    """ Return a universally-unique dataset name """
    return f'{prefix}-{uuid.uuid4().hex[:8]}'


def unique_project_description():
    """ Return a universally-unique project description """
    return ''.join([str(uuid.uuid4())[:6] for num in range(30)])


def load_credentials(path: str = 'credentials.txt', user_index: int = 0):
    """ Return tuple of username and password """
    assert os.path.exists(path), f"Specificy login credentials in {path}"
    with open(path) as cfile:
        lines = cfile.readlines()
        assert len(lines) >= 2, f"Must have line for username and password in {path}"
    # return username (first line) and password (second line)
    return lines[2 * user_index].strip(), lines[(2 * user_index) + 1].strip()


def valid_custom_docker_instruction():
    """ Return a valid custom Docker instruction"""
    return "RUN cd /tmp && git clone https://github.com/gigantum/confhttpproxy && cd /tmp/confhttpproxy && pip install -e."


def invalid_custom_docker_instruction():
    """ Return an invalid custom Docker instruction"""
    return "RUN /bin/false"


def is_container_stopped(driver):
    """ Check if the container is stopped """
    return driver.find_element_by_css_selector(".flex>.Stopped").is_displayed()


def stop_container(driver):
    """ Stop container after test is finished """
    return driver.find_element_by_css_selector(".flex>.Running").click()


def file_drag_drop(driver):
    """ Drag and drop a file into the file browser """
    js_script = """for (var b = arguments[0], k = arguments[1], l = arguments[2], c = b.ownerDocument, m = 0;;) {
            var e = b.getBoundingClientRect(),
                g = e.left + (k || e.width / 2),
                h = e.top + (l || e.height / 2),
                f = c.elementFromPoint(g, h);
            if (f && b.contains(f)) break;
            if (1 < ++m) throw b = Error('Element not interractable'), b.code = 15, b;
            b.scrollIntoView({
                behavior: 'instant',
                block: 'center',
                inline: 'center'
            })
            }
        var a = c.createElement('INPUT');
        a.setAttribute('type', 'file');
        a.setAttribute('style', 'position:fixed;z-index:2147483647;left:0;top:0;');
        a.onchange = function(evt) {
            var b = {
                effectAllowed: 'all',
                dropEffect: 'none',
                types: ['Files'],
                files: this.files,
                setData: function() {},
                getData: function() {},
                clearData: function() {},
                setDragImage: function() {}
            };
            window.DataTransferItemList && (b.items = Object.setPrototypeOf([Object.setPrototypeOf({
                kind: 'file',
                type: this.files[0].type,
                file: this.files[0],
                getAsFile: function() {
                    return this.file
                },
                getAsEntry: function() {
                    console.log(evt)
                    console.log(this, this.file, b)
                    var isDirectory = this.file.name.indexOf(".") < 0
                    var isFile = this.file.name.indexOf(".") > -1
                    return {"file": this.file, "entry": { "fullpath": this.file.name, "file": this.file, 
                    "name": this.file.name, isDirectory: isDirectory, isFile: isFile}}
                },
                getAsString: function(b) {
                    var a = new FileReader;
                    a.onload = function(a) {
                        b(a.target.result)
                    };
                    a.readAsText(this.file)
                }
            }, DataTransferItem.prototype)], DataTransferItemList.prototype));
            Object.setPrototypeOf(b, DataTransfer.prototype);
            ['dragenter', 'dragover', 'drop'].forEach(function(a) {
                var d = c.createEvent('DragEvent');
                d.initMouseEvent(a, !0, !0, c.defaultView, 0, 0, 0, g, h, !1, !1, !1, !1, 0, null);
                Object.setPrototypeOf(d, null);
                d.dataTransfer = b;
                console.log(d)

                Object.setPrototypeOf(d, DragEvent.prototype);
                f.dispatchEvent(d)
            });
            a.parentElement.removeChild(a)
        };
        c.documentElement.appendChild(a);
        a.getBoundingClientRect();
        return a;"""
    try:
        drop_target = driver.find_element_by_css_selector(".FileBrowser")
        logging.info("Adding a file")
        file_path = '/tmp/sample-upload.txt'
        with open(file_path, 'w') as example_file:
            example_file.write('Sample Text')
        file_input = driver.execute_script(js_script, drop_target, 0, 0)
        file_input.send_keys(file_path)
    except:
        # two different selectors for project file browser vs dataset file browser
        # below is the selector for dataset file browser
        drop_target = driver.find_element_by_css_selector(".FileBrowser__empty")
        logging.info("Adding a file")
        file_path = '/tmp/sample-upload.txt'
        with open(file_path, 'w') as example_file:
            example_file.write('Sample Text')
        file_input = driver.execute_script(js_script, drop_target, 0, 0)
        file_input.send_keys(file_path)


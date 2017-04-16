from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
import time
from random import uniform
import os
from os.path import isfile, join

def sellogin(browser, username = None, password = None):
    browser = selopner(browser, "https://www.chess.com/login")

    if username:
        browser.find_element_by_id("username").send_keys(username)
    if password:
        browser.find_element_by_id("password").send_keys(password)

    browser.find_element_by_id("login").click()


def selopner(browser, pointl):
    while True:
        try:
            browser.get(pointl)
            time.sleep(uniform(1, 3))
            return browser
        except Exception, errormsg:
            print repr(errormsg)

            print "something went wrong, reopening %s" %pointl
            time.sleep(uniform(5, 8))

def pickbrowser():
    return webdriver.Chrome(os.path.abspath("data/webdriver/chromedriver"))

def sendpmSel(browser, member, msg, delay):
    browser = selopner(browser, "https://www.chess.com/messages/compose/" + member.name)
    while True:
        try:
            browser.execute_script("tinyMCE.activeEditor.setContent('%s')" %msg)
            break
        except Exception, e:
            print repr(e)
            time.sleep(uniform(2, 3))

    browser.find_element_by_xpath("//*[@class='btn btn-primary btn-large']").click()
    time.sleep(uniform(delay, delay + 1))

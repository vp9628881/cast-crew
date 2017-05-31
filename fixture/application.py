from selenium import webdriver
from os import environ
from selenium.webdriver.remote.remote_connection import RemoteConnection
from sauceclient import SauceClient
import time

class Application:
    def __init__(self, browser_config, test_name):
        self.browser_config = browser_config
        self.test_name = test_name
        username = environ.get('SAUCE_USERNAME', 'vp9628881')
        access_key = environ.get('SAUCE_ACCESS_KEY', '35b7c665-60a3-4561-b197-bf0069ecf3d4')
        selenium_endpoint = "https://%s:%s@ondemand.saucelabs.com:443/wd/hub" % (username, access_key)
        self.sauce_client = SauceClient(username, access_key)
        build_tag = environ.get('BUILD_TAG', None)
        tunnel_id = environ.get('TUNNEL_IDENTIFIER', None)
        desired_cap = dict()
        desired_cap.update(self.browser_config)
        desired_cap['build'] = build_tag
        desired_cap['tunnelIdentifier'] = tunnel_id
        executor = RemoteConnection(selenium_endpoint, resolve_ip=False)
        desired_cap['name'] = self.test_name
        self.wd = webdriver.Remote(command_executor=executor, desired_capabilities=desired_cap)
        self.wd.implicitly_wait(60)

    def submit_contact_form(self):
        wd = self.wd
        wd.find_element_by_css_selector("input.button").click()
        time.sleep(float(15000) / 1000)
        assert("Thank you" in wd.find_element_by_tag_name("html").text)
        self.sauce_client.jobs.update_job(wd.session_id, passed=True)

    def fillout_contact_form(self, contact):
        wd = self.wd
        wd.find_element_by_id("avia_1_1").click()
        wd.find_element_by_id("avia_1_1").clear()
        wd.find_element_by_id("avia_1_1").send_keys(contact.firstname)
        wd.find_element_by_id("avia_2_1").click()
        wd.find_element_by_id("avia_2_1").clear()
        wd.find_element_by_id("avia_2_1").send_keys(contact.lastname)
        wd.find_element_by_id("avia_3_1").click()
        wd.find_element_by_id("avia_3_1").clear()
        wd.find_element_by_id("avia_3_1").send_keys(contact.email)
        wd.find_element_by_id("avia_4_1").click()
        wd.find_element_by_id("avia_4_1").clear()
        wd.find_element_by_id("avia_4_1").send_keys(contact.company)
        wd.find_element_by_id("avia_5_1").click()
        wd.find_element_by_id("avia_5_1").clear()
        wd.find_element_by_id("avia_5_1").send_keys(contact.subject)
        wd.find_element_by_id("avia_6_1").click()
        wd.find_element_by_id("avia_6_1").clear()
        wd.find_element_by_id("avia_6_1").send_keys(contact.message)

    def open_contact_form(self):
        wd = self.wd
        wd.find_element_by_xpath("//ul[@id='avia-menu']//span[.='Support']").click()
        wd.find_element_by_xpath("//ul[@id='avia-menu']//span[.='Contact']").click()

    def open_home_page(self):
        wd = self.wd
        wd.get("http://www.castandcrew.com/")

    def destroy(self):
        self.wd.quit()
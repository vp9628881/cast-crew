# -*- coding: utf-8 -*-
import pytest
from fixture.application import Application

browsers = [{"platform": "Windows 10",
        "browserName": "Firefox",
        "version": "49.0"
    }, {
        "platform": "OS X 10.12",
        "browserName": "firefox",
        "version": "49.0"
    }, {
        "platform": "Windows 7",
        "browserName": "internet explorer",
        "version": "11.0"}]

def pytest_generate_tests(metafunc):
    if "personal_info" in metafunc.fixturenames:
        metafunc.parametrize('browser_config',
                             browsers,
                             ids=_generate_param_ids('broswerConfig', browsers),
                             scope='function')

def _generate_param_ids(name, values):
    return [("<%s:%s>" % (name, value)).replace('.', '_') for value in values]

@pytest.fixture
def app(request, browser_config):
    test_name = request.node.name
    fixture = Application(browser_config, test_name)
    request.addfinalizer(fixture.destroy)
    return fixture


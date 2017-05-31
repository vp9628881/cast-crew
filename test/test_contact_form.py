# -*- coding: utf-8 -*-

from data.for_contact_form import testdata
import pytest

@pytest.mark.usefixtures()
@pytest.mark.parametrize("personal_info", testdata)
def test_test_contact_form(app, personal_info):
    app.open_home_page()
    app.open_contact_form()
    app.fillout_contact_form(personal_info)
    app.submit_contact_form()

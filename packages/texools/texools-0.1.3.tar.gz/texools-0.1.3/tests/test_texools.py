#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `texools` package."""

import pytest

from texools import asciify


# @pytest.fixture
# def response():
#     """Sample pytest fixture.
#
#     See more at: http://doc.pytest.org/en/latest/fixture.html
#     """
#     # import requests
#     # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')
#
#
# def test_content(response):
#     """Sample pytest test function with the pytest fixture as an argument."""
#     # from bs4 import BeautifulSoup
#     # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_asciify_args():
    assert asciify('Some text.')
    assert asciify('Good and ® © ℠')

    with pytest.raises(TypeError):
        asciify()
    with pytest.raises(TypeError):
        asciify(5)
    with pytest.raises(TypeError):
        asciify(list())
    with pytest.raises(TypeError):
        asciify('string 1', 'string 2')

import os
from typing import Text

import pytest

from texools.files import partspath


@pytest.fixture(autouse=True)
def mock_user_dir(monkeypatch):
    def mock_user_dir(path):
        return '/home/johnny'

    monkeypatch.setattr(os.path, 'expanduser', mock_user_dir)

    yield


class TestPartspath(object):
    def test_args(self):
        assert partspath('/home/johnny', 'Desktop')
        assert partspath('C:\\home\\johnny')

        with pytest.raises(ValueError):
            partspath()
        with pytest.raises(TypeError):
            partspath(dict())
        with pytest.raises(TypeError):
            partspath(list(), list())

    def test_return_types(self):
        assert isinstance(partspath('/home/johnny'), Text)
        assert isinstance(partspath('/home/johnny', 'Desktop'), Text)

    def test_return_values(self):
        assert partspath('/home/johnny') in ('/home/johnny', '\\home\\johnny')
        assert partspath('~') in ('/home/johnny', '\\home\\johnny')
        assert partspath('/home/johnny', 'Desktop') in (
            '/home/johnny/Desktop',
            '\\home\\johnny\\Desktop'
        )
        assert partspath('~/stuff', 'textfile.txt') in (
            '/home/johnny/stuff/textfile.txt',
            '\\home\\johnny\\stuff\\textfile.txt'
        )
        assert partspath('C:\\home\\johnny') in (
            'C:/home/johnny', 'C:\\home\\johnny'
        )
        assert partspath('C:/', 'Users', 'johnny') in (
            'C:/Users/johnny', 'C:\\Users\\johnny'
        )

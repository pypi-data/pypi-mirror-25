from typing import Text

import pytest

from texools.files import partspath


class TestPartspath(object):
    def test_args(self):
        assert partspath('/home/johnny', 'Desktop')
        assert partspath('C:\\home\\johnny')

        with pytest.raises(TypeError):
            partspath()
        with pytest.raises(TypeError):
            partspath(dict())
        with pytest.raises(TypeError):
            partspath(list(), list())

    def test_return_types(self):
        assert isinstance(partspath('/home/johnny'), Text)
        assert isinstance(partspath('/home/johnny', 'Desktop'), Text)

    def test_return_values(self):
        assert partspath('/home/johnny') == '/home/johnny'
        assert partspath('/home/johnny', 'Desktop') == '/home/johnny/Desktop'
        assert partspath('~/johnny', 'textfile.txt') == '~/johnny/textfile.txt'
        assert partspath('C:\\home\\johnny') == 'C:\\home\\johnny'
        assert partspath('C:', 'Users', 'johnny') == 'C:/Users/johnny'

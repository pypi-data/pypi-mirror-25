from typing import Text

import pytest

from texools.utils import textcheck, tabify


class TestTextcheck(object):
    def test_args(self):
        assert textcheck('Some text.')
        assert textcheck('Good and ® © ℠')
        assert textcheck('Good \n')

        with pytest.raises(TypeError):
            textcheck()
        with pytest.raises(TypeError):
            textcheck(5)
        with pytest.raises(TypeError):
            textcheck(list())
        with pytest.raises(TypeError):
            textcheck('string 1', 'string 2')

    def test_return_types(self):
        assert isinstance(textcheck('Some text.'), bool)
        assert isinstance(textcheck('Good and ® © ℠'), bool)
        assert isinstance(textcheck('Good \n'), bool)


class TestTabify(object):
    def test_args(self):
        assert tabify(',')
        assert tabify('|')
        assert tabify('\t')
        assert tabify('TAB')
        assert tabify('tab')

        with pytest.raises(TypeError):
            tabify()
        with pytest.raises(TypeError):
            tabify(5)
        with pytest.raises(TypeError):
            tabify(list())
        with pytest.raises(TypeError):
            tabify(',', '|')

    def test_return_types(self):
        assert isinstance(tabify(','), Text)
        assert isinstance(tabify('|'), Text)
        assert isinstance(tabify('\t'), Text)
        assert isinstance(tabify('tab'), Text)
        assert isinstance(tabify('TAB'), Text)

    def test_return_values(self):
        assert tabify(',') == ','
        assert tabify('|') == '|'
        assert tabify('\t') == '\t'
        assert tabify('tab') == '\t'
        assert tabify('TAB') == '\t'

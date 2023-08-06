from typing import Text

import pytest

from texools.strings import asciify


class TestAsciify(object):
    def test_args(self):
        assert asciify('Some text.')
        assert asciify('Good and ® © ℠')
        assert asciify('Good \n')

        with pytest.raises(TypeError):
            asciify()
        with pytest.raises(TypeError):
            asciify(5)
        with pytest.raises(TypeError):
            asciify(list())
        with pytest.raises(TypeError):
            asciify('string 1', 'string 2')

    def test_return_types(self):
        assert isinstance(asciify('Some text.'), Text)
        assert isinstance(asciify('Good and ® © ℠'), Text)
        assert isinstance(asciify('Good \n'), Text)

    def test_return_values(self):
        assert asciify('Some text.') == 'Some text.'
        assert asciify('Good and ® © ℠') == 'Good and   '
        assert asciify('Good \n') == 'Good '
        assert asciify('Good  ') == 'Good  '
        assert asciify('\n') == ''
        assert asciify('\t') == '\t'

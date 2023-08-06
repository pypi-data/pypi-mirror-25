from typing import Text

import pytest

from texools.files import new_file_check, partspath


class TestPartspath(object):
    partspath_raises_params = [
        (), (dict()), (list(), list()), ('', ''), (13,), (None,),
        (None,), (None, None), ('C:/', None), (12, 'directory')
    ]
    partspath_return_types = [
        ('/home/johnny',), ('/home/johnny', 'Desktop'),
        ('C:\\Users\\johnny',), ('C:\\Users\\johnny', 'Pictures'),
        ('\\\\server1', 'directory_1'), ('//server1', 'directory_1')
    ]
    partspath_return_expected = [
        (('/home/johnny',), ('/home/johnny', '\\home\\johnny')),
        (('~',), ('/home/johnny', '\\home\\johnny')),
        (('/home/johnny', 'Desktop'), ('/home/johnny/Desktop',
                                       '\\home\\johnny\\Desktop')),
        (('~/stuff', 'textfile.txt'), ('/home/johnny/stuff/textfile.txt',
                                       '\\home\\johnny\\stuff\\textfile.txt')),
        (('C:\\home\\johnny',), ('C:/home/johnny', 'C:\\home\\johnny')),
        (('C:/', 'Users', 'johnny'), ('C:/Users/johnny', 'C:\\Users\\johnny')),
        (('\\\\server1', 'directory_1'), ('\\server1\\directory_1',
                                          r'\\server1/directory_1',
                                          '//server1/directory_1'))
    ]

    @pytest.mark.parametrize('parts', partspath_raises_params)
    def test_raises(self, parts):
        with pytest.raises(TypeError):
            partspath(*parts)

    @pytest.mark.parametrize('parts', partspath_return_types)
    def test_partspath_return_types(self, parts):
        assert isinstance(partspath(*parts), Text)

    @pytest.mark.parametrize('parts, expected', partspath_return_expected)
    def test_return_values(self, mock_user_dir, parts, expected):
        assert partspath(*parts) in expected


class TestNewFileCheck(object):
    new_file_check_raises_params = [
        (13, dict()), ('', ''), (None, None), ('C:/', None), (12, 'directory')
    ]

    @pytest.mark.parametrize('infile_path, outfile_path',
                             new_file_check_raises_params)
    def test_raises(self, infile_path, outfile_path):
        with pytest.raises(TypeError):
            new_file_check(infile_path, outfile_path)

import os

import pytest


@pytest.fixture()
def mock_user_dir(monkeypatch):
    def mock_dir(path):
        return '/home/johnny'

    monkeypatch.setattr(os.path, 'expanduser', mock_dir)
    yield
    monkeypatch.undo()


@pytest.fixture()
def mock_file_mtime(monkeypatch):
    def mock_mtime(path):
        mtimes_dict = {
            'source_older.csv': 1506295001.0244,
            'processed_newer.csv': 1506295196.7252,
            'source_newer.csv': 1506295196.7252,
            'processed_older.csv': 1506295001.0244,
        }
        base_name = os.path.basename(path)
        return mtimes_dict[base_name]

    monkeypatch.setattr(os.path, 'getmtime', mock_mtime)
    yield
    monkeypatch.undo()

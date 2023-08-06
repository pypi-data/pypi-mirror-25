import os
from pathlib import Path
from typing import Text

from .utils import textcheck


def partspath(*parts: Text) -> Text:
    """
    Take path parts and return a joined and normalized filepath.
    """

    if parts:
        for p in parts:
            textcheck(p)
        if parts[0].startswith('~'):
            parts = list(parts)
            parts[0] = parts[0].replace('~', os.path.expanduser('~'))
            parts = tuple(parts)
        return str(Path(*parts))
    else:
        raise ValueError("Text value(s) with len() > 0 must be passed")



def new_file_check(infile_path: Text, outfile_path: Text,
                   force: bool = False) -> bool:
    """
    Checks for existence of new source file to process.
    1. If force then return True.
    2. If outfile_path doesn't exist then return True
    3. If outfile_path exists and infile_path is newer than outfile_path
    then return True.
    4. Else return False
    """

    if force:
        return True
    elif not os.path.exists(outfile_path):
        return True
    else:
        if os.path.getmtime(infile_path) >= os.path.getmtime(outfile_path):
            return True
        else:
            return False

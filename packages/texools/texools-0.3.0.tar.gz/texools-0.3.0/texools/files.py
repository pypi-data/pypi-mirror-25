from pathlib import Path

import os


def partspath(*parts: str) -> str:
    """
    Take path parts and return a joined and normalized filepath.
    """

    if parts:
        for part in parts:
            if not part:
                raise TypeError("func requires non-empty str but emptry str "
                                "or None passed.")
            elif not isinstance(part, str):
                raise TypeError("func requires str but "
                                "{0} was passed.".format(type(part).__name__))
        if parts[0].startswith('~'):
            parts = list(parts)
            parts[0] = parts[0].replace('~', os.path.expanduser('~'))
            parts = tuple(parts)
        return os.path.normpath(str(Path(*parts)))
    else:
        raise TypeError("func requires str argument(s) but empty str "
                        "or None passed.")


def new_file_check(infile_path: str, outfile_path: str,
                   force: bool = False) -> bool:
    """
    Checks for existence of new source file to process.
    1. If force = True or outfile_path doesn't exist return True
    2. If outfile_path exists and infile_path is newer than outfile_path
    then return True.
    4. Else return False
    """

    if isinstance(infile_path, str) and isinstance(outfile_path, str) \
            and infile_path and outfile_path:
        if force or not os.path.exists(outfile_path):
            return True
        else:
            if os.path.getmtime(infile_path) > os.path.getmtime(outfile_path):
                return True
            else:
                return False
    else:
        raise TypeError("Both infile_path and outfile_path must be str. {0} "
                        "(infile_path) and {1} (outfile_path) were passed."
                        "".format(type(infile_path).__name__,
                                  type(outfile_path).__name__))

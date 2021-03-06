""" Skeleton class for importing files """

import gzip

from pathlib import Path
from typing import Union


__all__ = [
    'Importer',
    'get_dataset_path'
]


class Importer(object):

    def __init__(self, filename=None):
        self.filename = str(filename) if filename else None
        self.data = []
        self.headers = None

        self.read_file()
        self.validate()

    def read_file(self):
        decode_required = False
        if self.filename.endswith("gz"):
            open_function = gzip.open
            decode_required = True
        else:
            open_function = open

        header_read = False

        with open_function(self.filename) as f:
            for line in f:
                if decode_required:
                    # this is needed if we are using gzip, which returns a
                    # binary-string.
                    line = line.decode('utf-8')
                line = line.strip()
                if not header_read:
                    self.headers = line.split("\t")
                    header_read = True
                else:
                    self.data.append(line.split("\t"))

    def validate(self):
        columns = len(self.data[1])
        for row in self.data:
            if len(row) != columns:
                raise Exception("Inconsistent number of rows")


def get_dataset_path(filename: Union[str, Path]) -> Path:
    """Return the filesystem path to the packaged data file.

    Parameters
    ----------
    filename : str, pathlib.Path
        The full name of the packaged data file.

    Return
    ------
    path : pathlib.Path
        The filesystem path to the packaged data file.

    Examples
    --------
    >>> from edgePy.io import get_dataset_path
    >>> str(get_dataset_path("GSE49712_HTSeq.txt.gz"))  # doctest:+ELLIPSIS
    '.../edgePy/data/GSE49712_HTSeq.txt.gz'

    """
    import edgePy
    directory = Path(edgePy.__file__).expanduser().resolve().parent
    return directory / 'data' / filename

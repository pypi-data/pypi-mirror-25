from unittest import mock

import pytest


@mock.patch('os.path.expanduser', return_value="/tmp")
def test_home_folder(mock):
    from salty.config import paths
    print(paths.home)

if __name__ == '__main__':
    test_home_folder()
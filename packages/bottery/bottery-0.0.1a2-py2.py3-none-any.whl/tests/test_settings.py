import contextlib
import os
import tempfile
from unittest import mock

import pytest

from bottery.conf import global_settings
from bottery.conf.settings import LazySettings, Settings


@contextlib.contextmanager
def tmp_project():
    '''
    Simulates a project directory with a random temporary directory and
    an empty settings.py file.
    '''

    # Save current directory to get back once the context is exited
    current_dir = os.getcwd()

    with tempfile.TemporaryDirectory() as tempdir:
        # Enters at the temporary directory
        os.chdir(tempdir)

        # Creates the empty settings.py
        settings_path = os.path.join(tempdir, 'settings.py')
        open(settings_path, 'w').close()

        try:
            yield
        finally:
            # When the context stoped being used, get back to
            # previously directory
            os.chdir(current_dir)


def test_settings_not_found():
    with pytest.raises(Exception):
        Settings()


def test_settings_with_global_settings_attrs():
    with tmp_project():
        settings = Settings()
        for attr in dir(global_settings):
            if not attr.isupper():
                continue

            _global = getattr(global_settings, attr)
            _local = getattr(settings, attr)
            assert _local == _global

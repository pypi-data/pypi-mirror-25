from __future__ import absolute_import, print_function, unicode_literals

from distutils.version import LooseVersion


def test_version_number_is_valid():
    from zenaton.version import __version__
    assert __version__
    assert LooseVersion(__version__)

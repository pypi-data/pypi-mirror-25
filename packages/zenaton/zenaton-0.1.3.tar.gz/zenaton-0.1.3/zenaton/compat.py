from __future__ import absolute_import, print_function, unicode_literals

try:
    from json.decoder import JSONDecodeError  # Python >= 3.5
except ImportError:
    JSONDecodeError = ValueError

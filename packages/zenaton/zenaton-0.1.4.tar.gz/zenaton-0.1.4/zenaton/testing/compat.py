try:
    # Included with Python >= 3.3
    from unittest.mock import MagicMock, call, patch  # noqa
except ImportError:
    from mock import MagicMock, call, patch  # noqa

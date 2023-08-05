from __future__ import absolute_import, print_function, unicode_literals

from zenaton.serialization import Serializable


class Task(Serializable):
    """
    Base class for tasks.
    """

    def handle(self):
        """
        You need to implement this method in your derived class.
        """
        raise NotImplementedError  # pragma: nocover

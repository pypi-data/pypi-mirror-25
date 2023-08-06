from __future__ import absolute_import, print_function, unicode_literals


class Position:

    SEP_ASYNC = 'a'
    SEP_PARALLEL = 'p'

    def __init__(self):
        self.main = 0
        self.position_str = '0'
        self.counter = 0

    def __str__(self):
        return self.position_str

    def __repr__(self):
        return '<Position({})>'.format(repr(self.position_str))

    def next(self):
        self.main += 1
        self.position_str = str(self.main)

    def next_parallel(self):
        if self.is_parallel():
            self.counter += 1
        else:
            self.main += 1
            self.counter = 0
        self.position_str = '{}{}{}'.format(
            self.main,
            self.SEP_PARALLEL,
            self.counter,
        )

    def is_parallel(self):
        return self.position_str.find(self.SEP_PARALLEL) >= 0

    def next_async(self):
        self.main += 1
        self.position_str = '{}{}'.format(
            self.main,
            self.SEP_ASYNC,
        )

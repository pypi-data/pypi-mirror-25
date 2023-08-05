from __future__ import absolute_import, print_function, unicode_literals

from zenaton import Workflow

from .provider_a import (
    GetPrice as GetPriceFromProviderA,
    Order as OrderFromProviderA,
)
from .provider_b import (
    GetPrice as GetPriceFromProviderB,
    Order as OrderFromProviderB,
)


class ParallelWorkflow(Workflow):

    def __init__(self, item):
        self.item = item

    def handle(self):
        price_a, price_b = self.execute(
            GetPriceFromProviderA(item=self.item),
            GetPriceFromProviderB(item=self.item),
        )

        if price_a <= price_b:
            self.execute(OrderFromProviderA(item=self.item))
        else:
            self.execute(OrderFromProviderB(item=self.item))

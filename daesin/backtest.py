from zipline.api import order_target, record, symbol
from zipline.algorithm import TradingAlgorithm
from zipline.api import set_commission, commission

class backtest():
    def __init__(self, data):
        self.data = data
        pass

    def run(self):
        def initialize(context):
            set_commission(commission.PerDollar(cost=0.00165))

        def handle_data(context, data):
            sym = symbol('GS')
            order_target(sym, 1)
        algo = TradingAlgorithm(capital_base=10000000, initialize=initialize, handle_data=handle_data)
        self.results = algo.run(self.data)

import pandas_datareader.data as web
import datetime
from zipline.api import order_target, record, symbol
from zipline.algorithm import TradingAlgorithm
import matplotlib.pyplot as plt
from zipline.api import set_commission, commission

start = datetime.datetime(2015, 1, 1)
end = datetime.datetime(2016, 1, 31)
gs = web.DataReader("078930.KS", "yahoo", start, end)
gs = gs[['Adj Close']]
gs.columns = ['GS']
gs = gs.tz_localize("UTC")

def initialize(context):
    set_commission(commission.PerDollar(cost=0.00165))

def handle_data(context, data):
    sym = symbol('GS')
    order_target(sym, 1)

algo = TradingAlgorithm(capital_base=10000000, initialize=initialize, handle_data=handle_data)
results = algo.run(gs)

results['portfolio_value'].plot()
plt.show()


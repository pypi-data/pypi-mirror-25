config = """# encoding:utf-8
from fxdayu_data.data_api import *
from fxdayu_data import MongoHandler


handler = MongoHandler()
client = handler.client


candle = Candle()
candle.set(handler, H="Stock_H", D="Stock_D")
candle.set_adjust(Adjust.db(client['adjust']))


factor = Factor()
factor.set(handler, "factor")


info = MongoInfo()
info.set(client['info'])
"""
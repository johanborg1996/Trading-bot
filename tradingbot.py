from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime

API_key =""
API_secret =""
BASE_URL =" https://demo-api.ig.com/gateway/deal"

ALPACAS_CREDS = {
    "API_KEY": API_key,
    "API_SECRET": API_secret,
    "PAPER": True
}

class MLTrader(Strategy):
    def initialize(self, symbol:str="SPY"):
        self.symbol = symbol
        self.sleeptime = "24H"
        self.lasttrade = None

        
    def on_trading_iteration(self):
        if self.lasttrade == None:
            order  = self.create_order(self.symbol, 10, "BUY")
            self.submit_order(order)
            self.lasttrade = "BUY"


#Must change s
#broker = Alpaca(ALPACAS_CREDS)   

#strategy = MLTrader(name='mlstrat', broker=broker, parameters={"symbol": "SPY"})

MLTrader.backtest(
    YahooDataBacktesting,
    start_date=datetime(2023, 12, 15),
    end_date=datetime(2023, 12, 31)
)
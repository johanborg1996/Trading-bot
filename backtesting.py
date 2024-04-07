from datetime import datetime

from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies import Strategy

from lumibot.brokers import Alpaca
from alpaca_trade_api import REST
from timedelta import Timedelta

API_key =""
API_secret =""
BASE_URL =" https://demo-api.ig.com/gateway/deal"


ALPACAS_CREDS = {
    "API_KEY": API_key,
    "API_SECRET": API_secret,
    "PAPER": True
}

# A simple strategy that buys AAPL on the first day and hold it
# Cash at risk is how much of the portfolio you want to use for each trade
class MLTrader(Strategy):
    def initialize(self, symbol:str="SPY", cash_at_risk:float=0.5):
        self.symbol = symbol
        self.sleeptime = "24H"
        self.lasttrade = None
        self.cash_at_risk = cash_at_risk
        self.api = REST(base_url=BASE_URL, api_key=API_key, api_secret=API_secret)

    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing() 

        if cash > last_price:
            if self.first_iteration:
                price = self.get_last_price(self.symbol)
                order = self.create_order(self.symbol, 
                                          quantity,
                                          "buy",
                                          type="bracket",
                                          take_profit_price=last_price*1.2,
                                          stop_loss_price=last_price*0.95)
                self.submit_order(order)
                self.lasttrade = "buy"
    
    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = cash * self.cash_at_risk // last_price
        return cash, last_price, quantity
    
    def get_news(self):
        pass



# Pick the dates that you want to start and end your backtest
# and the allocated budget
backtesting_start = datetime(2023, 12, 15)
backtesting_end = datetime(2023, 12, 31)

# broker = Alpaca(ALPACAS_CREDS)

# strategy = MLTrader(name='mlstrat', 
#                     broker=broker, 
#                     parameters={"symbol": "SPY", "cash_at_risk": 0.5})


# Run the backtest
MLTrader.backtest(
    YahooDataBacktesting,
    backtesting_start,
    backtesting_end,
    parameters={"symbol": "SPY", "cash_at_risk": 0.5}
)
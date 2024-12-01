from datetime import datetime

from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies import Strategy

from lumibot.brokers import Alpaca
from alpaca_trade_api import REST
from timedelta import Timedelta

import properties

API_KEY = properties.API_KEY
API_SECRET = properties.API_SECRET
BASE_URL = properties.BASE_URL


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
        self.api = REST(base_url=BASE_URL, key_id=API_key, secret_key=API_secret)

    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing() 

        if cash > last_price:
            if self.lasttrade == None:
                news = self.get_news()
                print(news)
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
    
    def get_dates(self):
        today = self.get_datetime()
        three_days_prior = today - Timedelta(days=3)
        return today.strftime("%Y-%m-%d"), three_days_prior.strftime("%Y-%m-%d")

    def get_news(self):
        today, three_days_prior = self.get_dates()
        self.api.get_news(symbol=self.symbol, 
                          start=three_days_prior, 
                          end=today)
        
        news = [ev.__dict__["_raw"]["headline"] for ev in news]
        return news



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
from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA

class UnderTwentyStrategy(Strategy):
    def __init__(self):
        self.tickers = ["SPY", "IWM", "QQQ", "VXX", "AAPL", "GOOGL", "FB", "AMZN"]  # Example tickers

    @property
    def assets(self):
        return self.tickers
    
    @property
    def interval(self):
        return "1day"
    
    @property
    def data(self):
        return []  # No additional data needed for this strategy

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            ohlcv = data["ohlcv"]
            
            # Ensure there is enough data
            if len(ohlcv) < 50:  # Assuming a 50-day SMA as our "long-term"
                continue
            
            # Compute SMAs
            short_sma = SMA(ticker, ohlcv, 20)  # 20-day SMA for "short-term"
            long_sma = SMA(ticker, ohlcv, 50)  # 50-day SMA for "long-term"
            current_price = ohlcv[-1][ticker]["close"]
            
            # Check for crossover and price under $20
            if short_sma[-1] > long_sma[-1] and current_price <= 20:
                # Allocate equally among tickers meeting criteria; adjust according to preference
                allocation_dict[ticker] = 1 / len(self.tickers)
            else:
                allocation_dict[ticker] = 0
        
        return TargetAllocation(allocation_dict)
from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "AAPL"  # Example ticker, change as needed

    @property
    def interval(self):
        return "1day"  # Interval for data fetching

    @property
    def assets(self):
        return [self.ticker]  # Assets to be considered

    def run(self, data):
        short_window = 40  # Short term window for SMA
        long_window = 100  # Long term window for SMA
        
        # Check if enough data is available
        if len(data["ohlcv"]) >= long_window:
            # Calculate the short and long moving averages
            short_sma = SMA(self.ticker, data["ohlcv"], length=short_window)[-1]
            long_sma = SMA(self.ticker, data["ohlcv"], length=long_window)[-1]
            
            # Determine the allocation
            if short_sma > long_sma:
                # Short MA is above long MA, signal to buy
                allocation = {"AAPL": 1}  # 100% investment in AAPL
            else:
                # Short MA is below long MA, signal to sell/hold
                allocation = {"AAPL": 0}  # 0% investment in AAPL
        else:
            # Not enough data
            allocation = {}
        
        return TargetAllocation(allocation)
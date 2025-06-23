from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA  # Importing just for example, adjust based on needs

class Under20NonEquityStrategy(Strategy):
    def __init__(self):
        # Initial set of tickers could be broader to encompass various asset classes,
        # but for the sake of this example, we'll keep it simple and focused.
        self.tickers = ["SPY", "QQQ", "USO", "SLV", "GLD"]
        # No additional data, assuming price is directly available from "ohlcv"
        self.data_list = []

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        allocation_dict = {}
        total_assets_under_20 = 0

        # Loop through each asset, check if it's under $20
        for ticker in self.tickers:
            ohlcv = data["ohlcv"]
            if ohlcv and ohlcv[-1][ticker]["close"] <= 20:
                total_assets_under_20 += 1
        
        # If there are assets under $20, allocate investment evenly among them
        if total_assets_under_20 > 0:
            allocation_per_asset = 1 / total_assets_under_20
            for ticker in self.tickers:
                if ohlcv[-1][ticker]["close"] <= 20:
                    allocation_dict[ticker] = allocation_per_asset
        else:
            # If no assets under $20, allocate nothing
            allocation_dict = {ticker: 0 for ticker in self.tickers}

        return TargetAllocation(allocation_dict)
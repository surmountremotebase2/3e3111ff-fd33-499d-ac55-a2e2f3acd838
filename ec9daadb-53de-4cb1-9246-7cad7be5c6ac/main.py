from surmount.base_class import Strategy, TargetAllocation
from surmount.data import BankPrimeLoanRate, ConsumerConfidence

class TradingStrategy(Strategy):
    def __init__(self):
        # We don't use tickers since we're not focusing on equities.
        self.data_list = [BankPrimeLoanRate(), ConsumerConfidence()]

    @property
    def interval(self):
        # Assuming our strategy doesn't require frequent updates
        return "1day"

    @property
    def assets(self):
        # List of assets being traded, could be a dummy if not trading equities
        return ["CASH"]

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        # Initial allocation to cash (or a money market fund) is 0
        cash_allocation = 0

        # Check if we have recent consumer confidence and bank prime loan rate data
        consumer_confidence_data = data.get(("consumer_confidence",))
        bank_prime_loan_rate_data = data.get(("bank_prime_loan_rate",))

        # Simple strategy: Increase cash allocation if consumer confidence is low
        # or the bank prime loan rate is high, indicating economic uncertainty
        if consumer_confidence_data and consumer_confidence_data[-1]['value'] < 100:
            cash_allocation += 0.5

        if bank_prime_loan_rate_data and bank_prime_loan_rate_data[-1]['value'] > 4:
            cash_allocation += 0.5

        # Ensure allocation does not exceed 1
        cash_allocation = min(1, cash_allocation)

        return TargetAllocation({"CASH": cash_allocation})
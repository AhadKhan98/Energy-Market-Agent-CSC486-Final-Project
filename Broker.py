from Tariff import Tariff
import random

class Broker():

    def __init__( self, idx ):

        ## ID number, cash balance, energy balance
        self.idx   = idx
        self.cash  = 0
        self.power = 0

        self.usage = None
        self.other = None

        ## Lists to contain:
        ##     asks: tuples of the form ( quantity, price )
        ##     tariffs: Tariff objects to submit to the market
        ##     customers: integers representing which customers are subscribed
        ##                to your tariffs.
        self.asks      = []
        self.tariffs   = []
        self.customers = []

    ## A function to accept the bootstrap data set.  The data set contains:
    ##     usage_data, a dict in which keys are integer customer ID numbers,
    ##                     and values are lists of customer's past usage profiles.
    ##     other_data, a dict in which 'Total Demand' is a list of past aggregate demand
    ##                 figures, 'Cleared Price' is a list of past wholesale prices,
    ##                 'Cleared Quantity' is a list of past wholesale quantities,
    ##                 and 'Difference' is a list of differences between cleared
    ##                 quantities and actual usage.
    def get_initial_data( self, usage_data, other_data ):

        self.usage = usage_data
        self.other = other_data

    ## Returns a list of asks of the form ( price, quantity ).
    def post_asks( self ):

        # Read past usage data
        past_data = {
        'Total Demand':[2427.584722,3133.841605,3305.694804],
        'Cleared Price':[41,39,44],
        'Cleared Quantity':[5400,6000,5500],
        'Difference':[2427.584722,3133.841605,3305.694804]}

        # Calculate the ask from the variables
        asks = []

        # Get average price and demand for all periods
        avg_price = sum(past_data['Cleared Price'])/len(past_data['Cleared Price'])
        avg_demand = sum(past_data['Total Demand'])/len(past_data['Total Demand'])

        # Iterate through all the periods to set asks
        for i in range(len(past_data['Total Demand'])):

            # Calculating price
            current_price = past_data['Cleared Price'][i]
            current_demand = past_data['Total Demand'][i]

            percent_difference = (current_demand/avg_demand)*100-100 # How much smaller or larger current demand is compared to avg demand

            if percent_difference < 0: # If current demand < avg demand
                # 0 - 25 percent smaller
                if abs(percent_difference) > 0 and abs(percent_difference) <= 25:
                    current_price -= random.randint(0,5)
                # 25 - 50 percent smaller
                elif abs(percent_difference) > 25 and abs(percent_difference) <= 50:
                    current_price -= random.randint(5,10)
                # 50 - 75 percent smaller
                elif abs(percent_difference) > 50 and abs(percent_difference) <= 75:
                    current_price -= random.randint(10,15)
                # 75+ percent smaller
                else:
                    current_price -= random.randint(15,20)
            else: # If current demand > avg demand
                if abs(percent_difference) > 0 and abs(percent_difference) <= 25:
                    current_price += random.randint(0,5)
                elif abs(percent_difference) > 25 and abs(percent_difference) <= 50:
                    current_price += random.randint(5,10)
                elif abs(percent_difference) > 50 and abs(percent_difference) <= 75:
                    current_price += random.randint(10,15)
                else:
                    current_price += random.randint(15,20)


            # Calculating Quantity
            quantity = int((past_data['Cleared Quantity'][i] + past_data['Difference'][i] + past_data['Total Demand'][i])/3)
            add_or_remove = random.randint(0,1) # Decides whether to add or remove from quantity
            add_or_remove_quantity = random.randint(0,500)
            if add_or_remove == 0:
                quantity -= add_or_remove_quantity
            else:
                quantity += add_or_remove_quantity

            # Append to final output
            asks.append((current_price,quantity))

        print(asks)
        return asks





    ## Returns a list of Tariff objects.
    def post_tariffs( self ):
        return [Tariff( self.idx, price=100, duration=3, exitfee=0 )]

    ## Receives data for the last time period from the server.
    def receive_message( self, msg ):
        pass

    ## Returns a negative number if the broker doesn't have enough energy to
    ## meet demand.  Returns a positive number otherwise.
    def get_energy_imbalance( self, data ):
        demand = sum( [data[i] for i in self.customers] )
        return self.power - demand

    def gain_revenue( self, customers, data ):
        for c in self.customers:
            self.cash += data[c] * customers[c].tariff.price

    ## Alter broker's cash balance based on supply/demand match.
    def adjust_cash( self, amt ):
        self.cash += amt

b= Broker(1)
b.post_asks()

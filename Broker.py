from Tariff import Tariff
import csv

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
        usage_for_c_5 = usage_data[5]
        print(usage_for_c_5)

    ## Returns a list of asks of the form ( price, quantity ).
    def post_asks( self ):
        return [ (i,100) for i in range(1,101) ]

    ## Returns a list of Tariff objects.
    
    def post_tariffs( self ):
    #     f = open('GenCos.csv', 'r')
    #     print(f.name)
    #     f.close()
    
     with open('OtherData.csv', 'r') as f: 
            for line in f: 
                print(line, end = '')
        
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

import pandas as pd
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('ggplot')
pd.options.display.float_format = '{:.3f}'.format

def execute_simulations(
        Scenario,
        Income,
        IYearGrowth,
        Expenses,
        EYearGrowth,
        SavingsInitial,
        PropertyPrice,
        PPYearGrowth,
        Years,
        DepositRate,
        Rent,
        RYearGrowth,
        MortgageRate,
        MortgageTermMonths):
    output_table = pd.MultiIndex.from_product([
    Scenario,
    Income,
    IYearGrowth,
    Expenses,
    EYearGrowth,
    SavingsInitial,
    PropertyPrice,
    PPYearGrowth,
    Years,
    DepositRate,
    Rent,
    RYearGrowth,
    MortgageRate,
    MortgageTermMonths
    ],
    names = [
    'Scenario',
    'Income',
    'IYearGrowth',
    'Expenses',
    'EYearGrowth',
    'SavingsInitial',
    'PropertyPrice',
    'PPYearGrowth',
    'Years',
    'DepositRate',
    'Rent',
    'RYearGrowth',
    'MortgageRate',
    'MortgageTermMonths'
    ])
    output_table = pd.DataFrame(index = output_table).reset_index()
    for i in output_table.index:
        s = investing_simulator(
        Scenario = output_table.loc[i, 'Scenario'],
        Income = output_table.loc[i, 'Income'],
        IYearGrowth = output_table.loc[i, 'IYearGrowth'],
        Expenses = output_table.loc[i, 'Expenses'],
        EYearGrowth = output_table.loc[i, 'EYearGrowth'],
        SavingsInitial = output_table.loc[i, 'SavingsInitial'],
        PropertyPrice = output_table.loc[i, 'PropertyPrice'],
        PPYearGrowth = output_table.loc[i, 'PPYearGrowth'],
        Years = output_table.loc[i, 'Years'],
        DepositRate = output_table.loc[i, 'DepositRate'],
        Rent = output_table.loc[i, 'Rent'],
        RYearGrowth = output_table.loc[i, 'RYearGrowth'],
        MortgageRate = output_table.loc[i, 'MortgageRate'],
        MortgageTermMonths = output_table.loc[i, 'MortgageTermMonths']
        )
        output_table.loc[i, 'Capital'] =  s.execute()
    return output_table

class investing_simulator():
    
    def __init__(self,
                 Scenario,
                 Income, 
                 IYearGrowth,
                 Expenses, 
                 EYearGrowth, 
                 SavingsInitial, 
                 PropertyPrice, 
                 PPYearGrowth, 
                 Years, 
                 DepositRate, 
                 Rent,
                 RYearGrowth, 
                 MortgageRate,
                 MortgageTermMonths,
                 isDetailed=False):
        
        # Init variables
        self.Scenario = Scenario
        self.Income = Income
        self.IYearGrowth = IYearGrowth

        self.Expenses = Expenses
        self.EYearGrowth = EYearGrowth

        self.SavingsInitial = SavingsInitial

        self.PropertyPrice = PropertyPrice
        self.PPYearGrowth = PPYearGrowth

        self.Years = Years

        self.DepositRate = DepositRate

        self.Rent = Rent
        self.RYearGrowth = RYearGrowth

        self.MortgageRate = MortgageRate
        self.MortgageTermMonths = MortgageTermMonths
        self.isDetailed = isDetailed
        
    # Execute calculations
    def execute(self):
        self.get_structure()

        if self.Scenario == 'Rent&Buy':
            self.renting_buying()

        if self.Scenario == 'Only Renting':
            self.only_renting()

        if self.Scenario == 'Standard Mortgage':
            self.stardard_mortgage()

        if self.Scenario == 'Early Repayment Mortgage':
            self.mortgage_repayment()

        if self.isDetailed==True:
            self.get_charts()
#         print(self.Scenario, '{0}M'.format(round(self.cash_result()/1000000, 2)))

        return self.cash_result()

    def cash_result(self):
        return round(self.df.iloc[self.df.shape[0]-1, self.df.columns.get_loc('Capital')])
    
    def get_charts(self):
        fig, ax = plt.subplots(1,2, figsize=(15, 5))
        c1 = sns.lineplot(data=self.df[['Interest', 'Principal', 'MortgagePayment', 'Income', 'Expenses']], dashes=False, ax=ax[0])
        c1.set_title('Period Variables, K')
        ylabels = ['{:,.0f}'.format(x) + 'K' for x in c1.get_yticks()/1000]
        c1.set_yticklabels(ylabels)
        c1.legend(loc='upper right')

        c2 = sns.lineplot(data=self.df[['Balance', 'PropertyPrice', 'Capital', 'EndPropertyDebt']], dashes=False, ax=ax[1])
        c2.set_title('As of date Variables, M')
        ylabels = ['{:,.0f}'.format(x) + 'M' for x in c2.get_yticks()/1000000]
        c2.set_yticklabels(ylabels)
        c2.legend(loc='upper right')

    def get_structure(self):
        self.time_range = pd.date_range(date.today(), periods=self.Years*12, freq='MS')

        self.future_income = {y: round(self.Income*(1+self.IYearGrowth)**i) \
                              for i, y in enumerate(np.unique(self.time_range.year.values))}
        self.future_expenses = [round(self.Expenses*(1+self.EYearGrowth/12)**i) for i, y in enumerate(self.time_range)]
        self.future_house_price = [round(self.PropertyPrice*(1+self.PPYearGrowth/12)**i) for i, y in enumerate(self.time_range)]
        self.future_rent = {y: round(self.Rent*(1+self.RYearGrowth)**i) \
                              for i, y in enumerate(np.unique(self.time_range.year.values))}

        self.df = pd.DataFrame(index=self.time_range)
        self.df['Year'] = self.df.index.year
        self.df['Income'] = self.df['Year'].replace(self.future_income)
        self.df['Rent'] = self.df['Year'].replace(self.future_rent)
        self.df['Expenses'] = self.future_expenses
        self.df['PropertyPrice'] = self.future_house_price
        self.df['Balance'] = 0
        self.df['Capital'] = 0

        self.df['Interest'] = 0
        self.df['Principal'] = 0
        self.df['StartPropertyDebt'] = 0
        self.df['EndPropertyDebt'] = 0
        self.df['MortgagePayment'] = 0
        self.df['MortgageAdditionalPayment'] = 0

    def renting_buying(self):
        # Balance in first month
        self.df.iloc[0, self.df.columns.get_loc('Balance')] = \
                    self.SavingsInitial +\
                    self.df.iloc[0, self.df.columns.get_loc('Income')] -\
                    self.df.iloc[0, self.df.columns.get_loc('Expenses')] -\
                    self.df.iloc[0, self.df.columns.get_loc('Rent')]
        self.df.iloc[0, self.df.columns.get_loc('Capital')] = self.df.iloc[0, self.df.columns.get_loc('Balance')]

        # Balance in next months
        for i in range(0, self.df.shape[0]):
            if i>0:
                self.df.iloc[i, self.df.columns.get_loc('Balance')] =\
                    self.df.iloc[i-1, self.df.columns.get_loc('Balance')]*(1+self.DepositRate/12) +\
                    self.df.iloc[i, self.df.columns.get_loc('Income')] -\
                    self.df.iloc[i, self.df.columns.get_loc('Expenses')] -\
                    self.df.iloc[i, self.df.columns.get_loc('Rent')]

                self.df.iloc[i, self.df.columns.get_loc('Capital')] = self.df.iloc[i, self.df.columns.get_loc('Balance')]

                
        try:
            # How much months we need to buy the house
            month_to_buy = min([i for i, b in enumerate(list(self.df['Balance'] -\
                                                             self.df['PropertyPrice'] > 0)) if b==True])

            # Home purchasing
            self.df.iloc[month_to_buy, self.df.columns.get_loc('Balance')] = \
                        self.df.iloc[month_to_buy, self.df.columns.get_loc('Balance')] - \
                        self.df.iloc[month_to_buy, self.df.columns.get_loc('PropertyPrice')]



            # Balance in next months after home purchasing
            for i in range(0, self.df.shape[0]):
                if i>month_to_buy:
                    self.df.iloc[i, self.df.columns.get_loc('Balance')] =\
                        self.df.iloc[i-1, self.df.columns.get_loc('Balance')]*(1+self.DepositRate/12) +\
                        self.df.iloc[i, self.df.columns.get_loc('Income')] -\
                        self.df.iloc[i, self.df.columns.get_loc('Expenses')]

            self.df.iloc[i, self.df.columns.get_loc('Capital')] = self.df.iloc[i, self.df.columns.get_loc('Balance')] \
            + self.df.iloc[i, self.df.columns.get_loc('PropertyPrice')]
        except:
            self.df.iloc[i, self.df.columns.get_loc('Capital')] = self.df.iloc[i, self.df.columns.get_loc('Balance')]
    
        
    def only_renting(self):
        # Balance in first month
        self.df.iloc[0, self.df.columns.get_loc('Balance')] = \
                    self.SavingsInitial +\
                    self.df.iloc[0, self.df.columns.get_loc('Income')] -\
                    self.df.iloc[0, self.df.columns.get_loc('Expenses')] -\
                    self.df.iloc[0, self.df.columns.get_loc('Rent')]
        self.df.iloc[0, self.df.columns.get_loc('Capital')] = self.df.iloc[0, self.df.columns.get_loc('Balance')]

        # Balance in next months
        for i in range(0, self.df.shape[0]):
            if i>0:
                self.df.iloc[i, self.df.columns.get_loc('Balance')] =\
                    self.df.iloc[i-1, self.df.columns.get_loc('Balance')]*(1+self.DepositRate/12) +\
                    self.df.iloc[i, self.df.columns.get_loc('Income')] -\
                    self.df.iloc[i, self.df.columns.get_loc('Expenses')] -\
                    self.df.iloc[i, self.df.columns.get_loc('Rent')]
            self.df.iloc[i, self.df.columns.get_loc('Capital')] = self.df.iloc[i, self.df.columns.get_loc('Balance')]

    def stardard_mortgage(self):
        # Balance in first month
        self.df.iloc[0, self.df.columns.get_loc('Balance')] = \
                    self.SavingsInitial +\
                    self.df.iloc[0, self.df.columns.get_loc('Income')] -\
                    self.df.iloc[0, self.df.columns.get_loc('Expenses')]

        # Get the loan
        self.df.iloc[0, self.df.columns.get_loc('StartPropertyDebt')] =\
        self.df.iloc[0, self.df.columns.get_loc('PropertyPrice')] - self.SavingsInitial

        # Interest in current debt
        self.df.iloc[0, self.df.columns.get_loc('Interest')] =\
            self.df.iloc[0, self.df.columns.get_loc('StartPropertyDebt')]*self.MortgageRate/12

        # Annuity payment
        self.df.iloc[:, self.df.columns.get_loc('MortgagePayment')] =\
           self.df.iloc[0, self.df.columns.get_loc('StartPropertyDebt')]*\
            (self.MortgageRate/12 + (self.MortgageRate/12)/((1+self.MortgageRate/12)**(self.MortgageTermMonths)-1))
        
        # Check the size of mortgage payment
        if self.df.iloc[0, self.df.columns.get_loc('Income')] -\
               self.df.iloc[0, self.df.columns.get_loc('Expenses')] -\
               self.df.iloc[0, self.df.columns.get_loc('MortgagePayment')]<0:
            print("Mortgage is not available")
            return
        
        

        # Money for the loan repayment
        self.df.iloc[0, self.df.columns.get_loc('Principal')] =\
            self.df.iloc[0, self.df.columns.get_loc('MortgagePayment')] - self.df.iloc[0, self.df.columns.get_loc('Interest')]

        # Reset the balance
        self.df.iloc[0, self.df.columns.get_loc('Balance')] =\
                    self.df.iloc[0, self.df.columns.get_loc('Income')] -\
                    self.df.iloc[0, self.df.columns.get_loc('Expenses')] -\
                    self.df.iloc[0, self.df.columns.get_loc('MortgagePayment')]

        # Assing end property debt
        self.df.iloc[0, self.df.columns.get_loc('EndPropertyDebt')] =\
                    self.df.iloc[0, self.df.columns.get_loc('StartPropertyDebt')] -\
                    self.df.iloc[0, self.df.columns.get_loc('Principal')]

        self.df.iloc[0, self.df.columns.get_loc('Capital')] = self.df.iloc[0, self.df.columns.get_loc('Balance')] +\
            self.df.iloc[0, self.df.columns.get_loc('PropertyPrice')] -\
            self.df.iloc[0, self.df.columns.get_loc('EndPropertyDebt')]

        # Balance in next months
        for i in range(0, self.df.shape[0]):
            if i>0:

                # Check wheter we still have the debt
                if self.df.iloc[i-1, self.df.columns.get_loc('EndPropertyDebt')] > 1:

                    # 1 Assign start property debt
                    self.df.iloc[i, self.df.columns.get_loc('StartPropertyDebt')] =\
                    self.df.iloc[i-1, self.df.columns.get_loc('EndPropertyDebt')]

                    # 2 Calculate interest in start propert debt
                    self.df.iloc[i, self.df.columns.get_loc('Interest')] =\
                        self.df.iloc[i, self.df.columns.get_loc('StartPropertyDebt')]*self.MortgageRate/12

                    # 3 Calculate principal
                    self.df.iloc[i, self.df.columns.get_loc('Principal')] =\
                        self.df.iloc[i, self.df.columns.get_loc('MortgagePayment')] -\
                        self.df.iloc[i, self.df.columns.get_loc('Interest')]

                    # 3 Calculate end property debt
                    self.df.iloc[i, self.df.columns.get_loc('EndPropertyDebt')] =\
                        self.df.iloc[i, self.df.columns.get_loc('StartPropertyDebt')] -\
                        self.df.iloc[i, self.df.columns.get_loc('Principal')]


                else:
                    self.df.iloc[i, self.df.columns.get_loc('MortgagePayment')] = 0
                    self.df.iloc[i, self.df.columns.get_loc('Interest')] = 0
                    self.df.iloc[i, self.df.columns.get_loc('Principal')] = 0
                    self.df.iloc[i, self.df.columns.get_loc('StartPropertyDebt')] = 0
                    self.df.iloc[i, self.df.columns.get_loc('EndPropertyDebt')] = 0
                    
                  
                self.df.iloc[i, self.df.columns.get_loc('Balance')] =\
                    self.df.iloc[i-1, self.df.columns.get_loc('Balance')]*(1+self.DepositRate/12) +\
                    self.df.iloc[i, self.df.columns.get_loc('Income')] -\
                    self.df.iloc[i, self.df.columns.get_loc('Expenses')] -\
                    self.df.iloc[i, self.df.columns.get_loc('MortgagePayment')]

                self.df.iloc[i, self.df.columns.get_loc('Capital')] = self.df.iloc[i, self.df.columns.get_loc('Balance')] +\
                        self.df.iloc[i, self.df.columns.get_loc('PropertyPrice')] -\
                        self.df.iloc[i, self.df.columns.get_loc('EndPropertyDebt')]


                
                

    def mortgage_repayment(self):
        
        # Balance in first month
        self.df.iloc[0, self.df.columns.get_loc('Balance')] = \
                    self.SavingsInitial +\
                    self.df.iloc[0, self.df.columns.get_loc('Income')] -\
                    self.df.iloc[0, self.df.columns.get_loc('Expenses')]

        # Get the loan
        self.df.iloc[0, self.df.columns.get_loc('StartPropertyDebt')] = self.df.iloc[0, self.df.columns.get_loc('PropertyPrice')] -\
            self.df.iloc[0, self.df.columns.get_loc('Balance')]
        
        # Reset the balance
        self.df.iloc[0, self.df.columns.get_loc('Balance')] = 0

        # Interest on current debt
        self.df.iloc[0, self.df.columns.get_loc('Interest')] =\
            self.df.iloc[0, self.df.columns.get_loc('StartPropertyDebt')]*self.MortgageRate/12

        # Annuity payment calculation
        self.df.iloc[:, self.df.columns.get_loc('MortgagePayment')] =\
           self.df.iloc[0, self.df.columns.get_loc('StartPropertyDebt')]*\
            (self.MortgageRate/12 + (self.MortgageRate/12)/((1+self.MortgageRate/12)**(self.MortgageTermMonths)-1))
        
        # Check the size of mortgage payment
        if self.df.iloc[0, self.df.columns.get_loc('Income')] -\
               self.df.iloc[0, self.df.columns.get_loc('Expenses')] -\
               self.df.iloc[0, self.df.columns.get_loc('MortgagePayment')]<0:
            print("Mortgage is not available")
            return

        # No money left for additional payment
        self.df.iloc[0, self.df.columns.get_loc('MortgageAdditionalPayment')] = 0

        # Principal
        self.df.iloc[0, self.df.columns.get_loc('Principal')] =\
            self.df.iloc[0, self.df.columns.get_loc('MortgagePayment')] - self.df.iloc[0, self.df.columns.get_loc('Interest')]

        # Refresh end property debt
        self.df.iloc[0, self.df.columns.get_loc('EndPropertyDebt')] =\
                    self.df.iloc[0, self.df.columns.get_loc('StartPropertyDebt')] -\
                    self.df.iloc[0, self.df.columns.get_loc('Principal')]
        
        # Net capital at the end of the first month
        self.df.iloc[0, self.df.columns.get_loc('Capital')] = self.df.iloc[0, self.df.columns.get_loc('Balance')] +\
                        self.df.iloc[0, self.df.columns.get_loc('PropertyPrice')] -\
                        self.df.iloc[0, self.df.columns.get_loc('EndPropertyDebt')]
        
        # ==============
        
        # Balance in next months
        for i in range(0, self.df.shape[0]):
            if i>0:
                # Change mortgage payment due to the previus end debt
                self.df.iloc[i, self.df.columns.get_loc('MortgagePayment')] =\
                    self.df.iloc[i-1, self.df.columns.get_loc('EndPropertyDebt')]*\
                    (self.MortgageRate/12 + (self.MortgageRate/12)/((1+self.MortgageRate/12)**(self.MortgageTermMonths)-1))

                # All expenses
                self.df.iloc[i, self.df.columns.get_loc('Balance')] =\
                    self.df.iloc[i, self.df.columns.get_loc('Income')] -\
                    self.df.iloc[i, self.df.columns.get_loc('Expenses')] -\
                    self.df.iloc[i, self.df.columns.get_loc('MortgagePayment')]


                # Check wheter we still have the debt
                if self.df.iloc[i-1, self.df.columns.get_loc('EndPropertyDebt')] > 1:

                    # 1 Assign start property debt
                    self.df.iloc[i, self.df.columns.get_loc('StartPropertyDebt')] =\
                    self.df.iloc[i-1, self.df.columns.get_loc('EndPropertyDebt')]

                    # 2 Calculate interest in start property debt
                    self.df.iloc[i, self.df.columns.get_loc('Interest')] =\
                        self.df.iloc[i, self.df.columns.get_loc('StartPropertyDebt')]*self.MortgageRate/12

                    # 3 Calculate principal share in total payment
                    self.df.iloc[i, self.df.columns.get_loc('Principal')] =\
                        self.df.iloc[i, self.df.columns.get_loc('MortgagePayment')] -\
                        self.df.iloc[i, self.df.columns.get_loc('Interest')]

                    # 4 How much money we can pay additionaly
                    self.df.iloc[i, self.df.columns.get_loc('MortgageAdditionalPayment')] =\
                        self.df.iloc[i, self.df.columns.get_loc('Income')] -\
                        self.df.iloc[i, self.df.columns.get_loc('Expenses')] -\
                        self.df.iloc[i, self.df.columns.get_loc('MortgagePayment')]

                    # 5 Calculate the end property debt
                    self.df.iloc[i, self.df.columns.get_loc('EndPropertyDebt')] =\
                        self.df.iloc[i, self.df.columns.get_loc('StartPropertyDebt')] -\
                        self.df.iloc[i, self.df.columns.get_loc('Principal')] -\
                        self.df.iloc[i, self.df.columns.get_loc('MortgageAdditionalPayment')]

                    # If we overpay
                    if self.df.iloc[i, self.df.columns.get_loc('EndPropertyDebt')]<0:
                        # Reset the debt
                        self.df.iloc[i, self.df.columns.get_loc('EndPropertyDebt')] = 0

                        # Set delta as an additional payment
                        self.df.iloc[i, self.df.columns.get_loc('MortgageAdditionalPayment')] =\
                            self.df.iloc[i, self.df.columns.get_loc('StartPropertyDebt')] -\
                            self.df.iloc[i, self.df.columns.get_loc('Principal')]

                        
                    # Calculate the balance
                    self.df.iloc[i, self.df.columns.get_loc('Balance')] =\
                    self.df.iloc[i, self.df.columns.get_loc('Income')] -\
                    self.df.iloc[i, self.df.columns.get_loc('Expenses')] -\
                    self.df.iloc[i, self.df.columns.get_loc('MortgagePayment')] -\
                    self.df.iloc[i, self.df.columns.get_loc('MortgageAdditionalPayment')]
                    
                
                # if we the debt already repaid
                else:
                    self.df.iloc[i, self.df.columns.get_loc('MortgagePayment')] = 0
                    self.df.iloc[i, self.df.columns.get_loc('Interest')] = 0
                    self.df.iloc[i, self.df.columns.get_loc('Principal')] = 0
                    self.df.iloc[i, self.df.columns.get_loc('StartPropertyDebt')] = 0
                    self.df.iloc[i, self.df.columns.get_loc('EndPropertyDebt')] = 0
                    self.df.iloc[i, self.df.columns.get_loc('MortgageAdditionalPayment')] = 0

                    self.df.iloc[i, self.df.columns.get_loc('Balance')] =\
                    self.df.iloc[i-1, self.df.columns.get_loc('Balance')]*(1+self.DepositRate/12) +\
                    self.df.iloc[i, self.df.columns.get_loc('Income')] -\
                    self.df.iloc[i, self.df.columns.get_loc('Expenses')]
                    
                # Calculate net capital
                self.df.iloc[i, self.df.columns.get_loc('Capital')] = self.df.iloc[i, self.df.columns.get_loc('Balance')] +\
                    self.df.iloc[i, self.df.columns.get_loc('PropertyPrice')] -\
                    self.df.iloc[i, self.df.columns.get_loc('EndPropertyDebt')]
#                 print(self.df.iloc[i, self.df.columns.get_loc('Capital')])
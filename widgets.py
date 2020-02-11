from __future__ import print_function
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets

from tools import *

def sc_calc(
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
):
    Income = [Income]
    IYearGrowth = [IYearGrowth]
    Expenses = [Expenses]
    EYearGrowth = [EYearGrowth]
    SavingsInitial = [SavingsInitial]
    PropertyPrice = [PropertyPrice]
    PPYearGrowth = [PPYearGrowth]
    Years = [Years]
    DepositRate = [DepositRate]
    Rent = [Rent]
    RYearGrowth = [RYearGrowth]
    MortgageRate = [MortgageRate]
    MortgageTermMonths = [MortgageTermMonths]
    isDetailed = True
    Scenario = ['Standard Mortgage', 'Rent&Buy', 'Only Renting', 'Early Repayment Mortgage']

    output_table = execute_simulations(Scenario,
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
            )
    fig = plt.subplots(figsize=(15, 5))
    c1 = sns.barplot(data=output_table, x='Scenario', y='Capital');
    c1.set_title('Final result in cash, K')
    ylabels = ['{:,.0f}'.format(x) + 'K' for x in c1.get_yticks()/1000]
    c1.set_yticklabels(ylabels);
    return output_table

w1 = interactive(sc_calc, 
    Income = (50000, 500000, 50000),
    IYearGrowth = (0.01, 0.3, 0.02),
    Expenses = (10000, 100000, 5000),
    EYearGrowth = (0.01, 0.3, 0.02),
    SavingsInitial = (10000, 5000000, 500000),
    PropertyPrice = (1000000, 10000000, 500000),
    PPYearGrowth = (0.01, 0.3, 0.02),
    Years = (1, 30, 1),
    DepositRate = (0.01, 0.3, 0.02),
    Rent = (10000, 100000, 5000),
    RYearGrowth = (0.01, 0.2, 0.02),
    MortgageRate = (0.01, 0.4, 0.02),
    MortgageTermMonths = (60, 300, 10)
                )


def sc_analyse(param):
    Income = [200000]
    IYearGrowth = [0.08]
    Expenses = [50000]
    EYearGrowth = [0.06]
    SavingsInitial = [5000000]
    PropertyPrice = [10000000]
    PPYearGrowth = [0.04]
    Years = [11]
    DepositRate = [0.01]
    Rent = [50000]
    RYearGrowth = [0.08]
    MortgageRate = [0.1]
    MortgageTermMonths = [120]
    isDetailed = True
    Scenario = ['Standard Mortgage', 'Rent&Buy', 'Only Renting', 'Early Repayment Mortgage']
    
    if param == 'Income':
        Income = [200000, 300000, 400000]
       
    if param == 'IYearGrowth':
        IYearGrowth = [0.01, 0.03, 0.05, 0.1]
        
    if param == 'Expenses':
        Expenses = [10000, 30000, 60000, 80000]
    
    if param == 'EYearGrowth':
        EYearGrowth = [0.01, 0.03, 0.05, 0.1]
    
    if param == 'SavingsInitial':
        SavingsInitial = [10000, 50000, 100000, 200000]
        
    if param == 'PropertyPrice':
        PropertyPrice = [6000000, 8000000, 10000000, 12000000]
    
    if param == 'PPYearGrowth':
        PPYearGrowth = [0.01, 0.03, 0.05, 0.1]
        
    if param == 'Years':
        Years = [5, 10, 15, 20]
    
    if param == 'DepositRate':
        DepositRate = [0.01, 0.05, 0.1, 0.15, 0.20, 0.25]
        
    if param == 'Rent':
        Rent = [10000, 30000, 60000, 80000]
        
    if param == 'RYearGrowth':
        RYearGrowth = [0.01, 0.03, 0.05, 0.1]
        
    if param == 'MortgageRate':
        MortgageRate = [0.01, 0.03, 0.05, 0.1]
     
    if param == 'MortgageTerm':
        MortgageTermMonths = [60, 120, 180, 220]

    output_table = execute_simulations(Scenario,
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
            )
    fig = plt.subplots(figsize=(15, 5))

    for s in Scenario:
        c1 = sns.lineplot(data=output_table[output_table['Scenario']==s], x=param, y='Capital', label=s);
        c1.set_title('How capital influenced by the parameter, K')
        ylabels = ['{:,.0f}'.format(x) + 'K' for x in c1.get_yticks()/1000]
        c1.set_yticklabels(ylabels);
        
    return output_table

w3 = interactive(sc_analyse, 
                 param=[
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
                 ]
                )
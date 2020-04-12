# 1. What is the most effective way to solve housing problem?

## Abstract idea
Sooner or later, everyone must solve the problem of housing.
Basically we have just two options - buy or rent. 
However in practice, we also can decide not to buy a property at all or take a mortgage to start immediately living in your own appartment.
Let's figure out what will be the most effective strategy in a given economic conditions.


## Here we have 4 stategies:
1. **Only renting:** to rent an apartment and keep money on deposit without buying own property;
2. **Rent&buy:** to rent an apartment and keep money on deposit until you save up enough for a property purchase;
3. **Standard mortgage:** to get a mortgage and repay due to initial payment schedule;
4. **Early Repayment Mortgage:** to get a mortgage and constantly make early repayments;

## Considered economic parameters:
**Income** — income per month
**IYearGrowth** – annual change of income
**Expenses** – living expenses per month
**EYearGrowth** – annual change of living expenses
**SavingsInitial** – how much money you've aready saved
**PropertyPrice** – the price of property in the start point
**PPYearGrowth** –  annual change of property price
**Years** – observation period to compare results of different strategies
**DepositRate** – annual deposit rate
**Rent** – rent expenses per month
**RYearGrowth** – annual change of rent expenses
**MortgageRate** – annual mortgage rate
**MortgageTermMonths** – mortgage term in month

## How we choose the best strategy
At the end of the observed period we sell property (if we have) and compare positions in cash.


## Quick Start
1. Open interface notebook and find section "Strategy execution"
2. Enter numbers related to your personal finance (Income, Expeses etc.) and economic environment (Deposit Rate, Property price etc.)
3. Get the answer what strategy will be the most profitable
   
![alt text](mortgage-demo.gif "Strategy calculation demo")


## Understand relationship between parameters
1. Open interface notebook and find section "Parameters relationship"
2. Choose the parameter that will be considered as a variable while others will be constant
![alt text](parameters-relationship.gif "Parameters relationship")

## Model flaws
- Fixed annual growth rates in the long term lead to exponential growth
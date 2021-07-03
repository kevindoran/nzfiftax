#!/bin/bash/python

import enum
import pandas as pd
import logging
import argparse


"""
SHARESIES_COLS = ['Oder ID', 'Trade date', 'Instrument code', 'Market code',
    'Quantity', 'Price', 'Transaction type', 'Exchange rate', 'Exchange fee',
    'Transaction fee', 'Currency', 'Amount', 'Transaction method']
"""


def peak_holding_differential(transactions, ticker, start_amount=0):
    """Calculates the peak holding differential"""
    transactions = filter_by_ticker(transactions, ticker)
    cur = start_amount
    peak = start_amount
    for idx, row in transactions.iterrows():
        ttype = row['Transaction type']
        if ttype == 'BUY':
            cur += row['Quantity']
        elif ttype == 'SELL':
            cur -= row['Quantity']
        else:
            raise Exception(f'Unexpected transaction type: {ttype}.')
        peak = max(peak, cur)
    end_amount = cur
    peak_diff = max(0, min(peak - end_amount, peak - start_amount))
    return peak_diff


def filter_by_ticker(transactions, ticker):
    df = transactions.loc[lambda df : df['Instrument code'] == ticker, :]
    return df


def filter_by_exchanges(transactions, exchange_codes):
    def f(row):
        return row['Market code'] in exchange_codes
    idx = transactions.apply(f, axis=1)
    res = transactions[idx]
    return res


def filter_by_type(transactions, transaction_type):
    if not transaction_type in {'BUY', 'SELL'}:
        raise Exception(f'Unexpected transaction type: {transaction_type}')
    df = transactions.loc[ \
            lambda df : df['Transaction type'] == transaction_type, :]
    return df
            

def average_cost_nzd(transactions, ticker):
    ts = filter_by_type(filter_by_ticker(transactions, ticker), 'BUY')
    total_shares = ts['Quantity'].sum()
    total_cost = (ts['Amount'] * 1/ts['Exchange rate']).sum()
    average_cost = total_cost / total_shares
    return average_cost


def peak_holding_method(transactions, ticker):
    phd = peak_holding_differential(transactions, ticker)
    avg_cost = average_cost_nzd(transactions, ticker)
    factor = 0.05
    ans = factor * phd * avg_cost
    return ans


def gain_method(transactions, ticker):
    avg_cost = average_cost_nzd(transactions, ticker)
    sells = filter_by_type(filter_by_ticker(transactions, ticker), 'SELL')
    sell_amounts = sells['Amount'] * sells['Exchange rate']
    gains = sell_amounts - avg_cost * sells['Quantity']
    total_gain = gains.sum()
    total_gain = max(0, total_gain)
    return total_gain
    

def taxable_amount(transactions, ticker):
    phd = peak_holding_method(transactions, ticker)
    gain = gain_method(transactions, ticker)
    if phd <= gain:
        ans = phd
        logging.info(f'{ticker}. Using peak method (gain: {gain:.2f}, '
                     f'peak: {phd:.2f}).')
    else:
        ans = gain
        logging.info(f'{ticker}. Using gain method (gain: {gain:.2f}, '
                     f'peak: {phd:.2f}).')
    logging.info(f'{ticker}. Taxable amount is: {ans:.2f}')
    return ans


def list_tickers(transactions):
    return transactions['Instrument code'].unique().tolist()


def total_taxable_amount(transactions):
    # We are only dealing with NYSE, NASDAQ and ASX at the moment.
    exchanges = transactions['Market code'].unique()
    covered_exchanges = {'NYSE', 'NASDAQ', 'ASX'}
    ignored_exchanges = set(exchanges) - covered_exchanges
    logging.info(f'Transactions present on the following exchanges: '
                 f'{exchanges}')
    logging.warning(f'Including exchanges {covered_exchanges}.\nIgnoring: '
                 f'{ignored_exchanges}')
    transactions = filter_by_exchanges(transactions, covered_exchanges)
    ans = 0
    for t in list_tickers(transactions):
        ans += taxable_amount(transactions, t)
    return ans


def import_sharesies_csv(filepath):
    df = pd.read_csv(filepath, header=0)
    return df


def main():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='Path to Sharesies transaction csv file.')
    args = parser.parse_args()
    filepath = args.file
    transactions = import_sharesies_csv(filepath)
    taxable_amount = total_taxable_amount(transactions)
    logging.info(f'Total taxable amount: {taxable_amount:.2f}')
    print(f'{taxable_amount:.2f}')


if __name__ == '__main__':
    main()

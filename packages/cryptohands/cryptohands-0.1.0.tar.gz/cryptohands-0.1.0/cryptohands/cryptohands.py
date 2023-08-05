# -*- coding: utf-8 -*-

"""Main module."""
from __future__ import absolute_import
from bitex import Bitfinex, Poloniex
from coinbase.wallet.client import Client as CoinbaseClient
import json
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# Get Config
try:
    _abs_file_path = os.path.join(os.path.dirname(__file__), "../config.json")
except NameError:
    _abs_file_path = os.path.join(os.getcwd(), "config.json")
with open(_abs_file_path, 'r') as fp:
    _config = json.load(fp)

# Access Google Sheet
# Setup credentials
_scope = ['https://spreadsheets.google.com/feeds']
_credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    _config['sheets_auth'], _scope
)
_gc = gspread.authorize(credentials=_credentials)
# Get sheet
_gs = _gc.open_by_key(_config['sheet_id'])


def get_bitfinex_balances():
    # Setup BitFinex API
    _bf = Bitfinex(
        key=_config['bitfinex']['key'],
        secret=_config['bitfinex']['secret']
    )
    # Retrieve Wallets Balances
    bf_balance = _bf.balance().json()
    update = {
        "bitfinex": {li['currency']: li['amount'] for li in bf_balance}
    }
    return update


def get_coinbase_balances():
    _coinbase = CoinbaseClient(
        api_key=_config['coinbase']['key'],
        api_secret=_config['coinbase']['secret']
    )
    wallets = _coinbase.get_accounts()
    balances = {li.balance.currency: li.balance.amount for li in wallets.data}
    update = {
        "coinbase": balances
    }
    return update


def get_poloniex_balances():
    _poloniex = Poloniex(
        key=_config['poloniex']['key'],
        secret=_config['poloniex']['secret']
    )
    # Get Balances
    p_balance = _poloniex.balance().json()
    # Filter for positive balances
    pos_balances = {k: v for k, v in p_balance.items() if float(v) > 0.0}
    # put into simple submission format
    update = {
        "poloniex": pos_balances
    }
    # submit for update
    return update


def update_balance_sheet(balances):
    if not isinstance(balances, dict):
        raise ValueError(
            '(balances) is {0} instead of dict'
            .format(type(balances))
        )
    for this_e in balances.keys():
        # Get or create the right sheet
        try:
            ws = _gs.worksheet(this_e)
        except gspread.exceptions.WorksheetNotFound:
            ws = _gs.add_worksheet(
                title=this_e,
                rows=_config['max_currencies'],
                cols="20"
            )
        # Setup update batch job
        block = ws.range('A1:B' + _config['max_currencies'])
        nextblankrow_i = [
            (cell.row * 2 - 2)
            for cell in block[::2]
            if cell.value is ''
        ][0]
        if nextblankrow_i is 0:
            #  Now assuming virgin sheet, so set header row
            block[nextblankrow_i].value = 'Currency'
            block[nextblankrow_i + 1].value = 'Amount'
            nextblankrow_i += 2
        for this_c in balances[this_e].keys():
            try:
                this_ci = [
                    li.value
                    for li in block].index(this_c)
                # currency is already in list, update it
                block[this_ci + 1].value = balances[this_e][this_c]
            except ValueError:
                # currency isn't already in list, add it
                block[nextblankrow_i].value = this_c
                block[nextblankrow_i + 1].value = balances[this_e][this_c]
                nextblankrow_i += 2
        # Submit batch update
        ws.update_cells(block)


def update_all_balances():
    balances = {}
    if 'bitfinex' in _config:
        balances.update(get_bitfinex_balances())
    if 'poloniex' in _config:
        balances.update(get_poloniex_balances())
    if 'coinbase' in _config:
        balances.update(get_coinbase_balances())
    update_balance_sheet(balances)


if __name__ == "__main__":
    update_all_balances()

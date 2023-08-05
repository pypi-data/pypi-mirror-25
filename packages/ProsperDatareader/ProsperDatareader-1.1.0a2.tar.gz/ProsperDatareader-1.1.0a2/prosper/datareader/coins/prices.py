"""datareader.coins.prices.py: tools for fetching cryptocoin price data"""
from datetime import datetime
from os import path
from enum import Enum

import requests
import pandas as pd

import prosper.datareader.config as config
import prosper.datareader.exceptions as exceptions
import prosper.datareader.coins.info as info

LOGGER = config.LOGGER
HERE = path.abspath(path.dirname(__file__))

__all__ = ('get_orderbook_hitbtc', 'get_quote_hitbtc')


class OrderBook(Enum):
    """enumerator for handling order book info"""
    asks = 'asks'
    bids = 'bids'

def _listify(
        data,
        key_name
):
    """recast data from dict to list, compress keys into sub-dict

    Args:
        data (:obj:`dict`): data to transform (dict(dict))
        key_name (str): name to recast key to

    Returns:
        (:obj:`list`): fixed data

    """
    listified_data = []
    for key, value in data.items():
        row = dict(value)
        row[key_name] = key
        listified_data.append(row)

    return listified_data

def coin_list_to_symbol_list(
        coin_list,
        currency='USD',
        strict=False
):
    """convert list of crypto currencies to HitBTC symbols

    Args:
        coin_list (str or :obj:`list`): list of coins to convert
        currency (str, optional): currency to FOREX against
        strict (bool, optional): throw if unsupported ticker is requested

    Returns:
        (:obj:`list`): list of valid coins and tickers

    """
    valid_symbol_list = info.supported_symbol_info('symbol')

    symbols_list = []
    invalid_symbols = []
    for coin in coin_list:
        ticker = str(coin).upper() + currency
        if ticker not in valid_symbol_list:
            invalid_symbols.append(ticker)

        symbols_list.append(ticker)

    if invalid_symbols and strict:
        raise KeyError('Unsupported ticker requested: {}'.format(invalid_symbols))

    return symbols_list

COIN_TICKER_URI = 'http://api.hitbtc.com/api/1/public/{symbol}/ticker'
def get_ticker_hitbtc(
        symbol,
        uri=COIN_TICKER_URI
):
    """fetch quote for coin

    Notes:
        incurs a .format(ticker=symbol) call, be careful with overriding uri

    Args:
        symbol (str): name of coin-ticker to pull
        uri (str, optional): resource link

    Returns:
        (:obj:`dict`) or (:obj:`list`): ticker data for desired coin

    """
    full_uri = ''
    if not symbol:
        ## fetching entire ticker list ##
        full_uri = uri.replace(r'{symbol}/', '')
    else:
        full_uri = uri.format(symbol=symbol)

    req = requests.get(full_uri)
    req.raise_for_status()
    data = req.json()

    if not symbol:
        ## fetching entire ticker list ##
        data = _listify(data, 'symbol')

    return data

COIN_ORDER_BOOK_URI = 'http://api.hitbtc.com/api/1/public/{symbol}/orderbook'
def get_order_book_hitbtc(
        symbol,
        format_price='number',
        format_amount='number',
        uri=COIN_ORDER_BOOK_URI
):
    """fetch orderbook data

    Notes:
        incurs a .format(ticker=symbol) call, be careful with overriding uri

    Args:
        symbol (str): name of coin-ticker to pull
        format_price (str, optional): optional format helper
        format_amount (str, optional): optional format helper
        uri (str, optional): resource link

    Returns:
        (:obj:`dict`): order book for coin-ticker

    """
    params = {}
    #TODO: this sucks
    if format_price:
        params['format_price'] = format_price
    if format_amount:
        params['format_amount'] = format_amount

    full_uri = uri.format(symbol=symbol)
    req = requests.get(full_uri, params=params)
    req.raise_for_status()

    data = req.json()

    return data #return both bids/asks for other steps to clean up later

################################################################################

def get_quote_hitbtc(
        coin_list,
        currency='USD',
        logger=LOGGER
):
    """fetch common summary data for crypto-coins

    Args:
        coin_list (:obj:`list`): list of tickers to look up'
        currency (str, optional): currency to FOREX against
        logger (:obj:`logging.logger`, optional): logging handle

    Returns:
        (:obj:`pandas.DataFrame`): coin info for the day, JSONable

    """
    logger.info('Generating quote for %s -- HitBTC', config._list_to_str(coin_list))

    logger.info('--validating coin_list')
    ticker_list = coin_list_to_symbol_list(
        coin_list,
        currency=currency,
        strict=True
    )

    logger.info('--fetching ticker data')
    raw_quote = get_ticker_hitbtc('')
    quote_df = pd.DataFrame(raw_quote)

    logger.info('--filtering ticker data')
    quote_df = quote_df[quote_df['symbol'].isin(ticker_list)]
    quote_df = quote_df[list(quote_df.columns.values)].apply(pd.to_numeric, errors='ignore')
    quote_df['pct_change'] = (quote_df['last'] - quote_df['open']) / quote_df['open'] * 100

    logger.debug(quote_df)
    return quote_df

def get_orderbook_hitbtc(
        coin,
        which_book,
        currency='USD',
        logger=LOGGER
):
    """fetch current orderbook from hitBTC

    Args:
        coin (str): name of coin to fetch
        which_book (str): Enum, 'asks' or 'bids'
        currency (str, optional): currency to FOREX against

    logger (:obj:`logging.logger`, optional): logging handle

    Returns:
        (:obj:`pandas.DataFrame`): current coin order book

    """
    logger.info('Generating orderbook for %s -- HitBTC', coin)
    order_enum = OrderBook(which_book)  # validates which order book key to use

    logger.info('--validating coin')
    symbol = coin_list_to_symbol_list(
        [coin],
        currency=currency,
        strict=True
    )[0]

    logger.info('--fetching orderbook')
    raw_orderbook = get_order_book_hitbtc(symbol)[which_book]

    orderbook_df = pd.DataFrame(raw_orderbook, columns=['price', 'ammount'])
    orderbook_df['symbol'] = symbol
    orderbook_df['coin'] = coin
    orderbook_df['orderbook'] = which_book

    logger.debug(orderbook_df)
    return orderbook_df

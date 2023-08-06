#!/usr/bin/env python2


"""
Defines the models, calculations and formatting operations for transactions.
"""

from decimal import Decimal
# import datetime

from stocktracker import dollars
from stocktracker import utility


class Transaction(object):
    """Base class for an individual transaction."""

    # Class names to JSON keys.
    _class_names = {
        'Buy': 'purchases',
        'Sell': 'sales',
        'Transfer': 'cashTransfers',
        'Dividend': 'dividends',
        'Interest': 'interest',
        'CapGain': 'capitalGains',
        'Liquidation': 'liquidations',
        'SecurityTransfer': 'securityTransfers',
    }
    _keys = {}

    @staticmethod
    def key_from_class_name(class_name):
        """Returns the JSON key corresponding to a Transaction subclass."""
        assert class_name in Transaction._class_names
        return Transaction._class_names[class_name]

    @staticmethod
    def class_name_from_key(key):
        """Returns the Transaction class name corresponding to a JSON key."""
        if not Transaction._keys:
            for class_name in Transaction._class_names:
                Transaction._keys[Transaction._class_names[class_name]] = (
                    class_name)
        assert key in Transaction._keys
        return Transaction._keys[key]

    def __repr__(self):
        raise NotImplementedError


class Dividend(Transaction):
    """A dividend transaction."""
    # pylint: disable=too-many-arguments
    def __init__(self, date, symbol, amount, qualified, reinvested):
        self.date = date
        self.symbol = symbol
        self.amount = amount
        self.qualified = qualified
        self.reinvested = reinvested

    def __repr__(self):
        return 'Dividend(%r, %r, %r, %r, %r)' % (
            self.date, self.symbol, self.amount, self.qualified,
            self.reinvested)

    def __str__(self):
        return '%s  Dividend of %s from %s%s%s' % \
            (self.date, dollars.to_str(self.amount), self.symbol,
             ' (qualified)' if self.qualified else '',
             ' - reinvested' if self.reinvested else '')

    @staticmethod
    def from_decoded_json(data):
        """Creates a Dividend transaction from dictionary."""
        return Dividend(utility.from_js_date(data['date']), data['symbol'],
                        Decimal(data['amount']), data['qualified'],
                        data['wasReinvested'])


class CapGain(Transaction):
    """A capital gains transaction."""
    # pylint: disable=too-many-arguments
    def __init__(self, date, symbol, amount, long_term, reinvested):
        self.date = date
        self.symbol = symbol
        self.amount = amount
        self.long_term = long_term
        self.reinvested = reinvested

    def __repr__(self):
        return '%s  %s-Term Cap Gain of %s from %s%s' % (
            self.date,
            'Long' if self.long_term else 'Short',
            dollars.to_str(self.amount), self.symbol,
            ' - reinvested' if self.reinvested else '')

    @staticmethod
    def from_decoded_json(data):
        """Creates a CapGain transaction from a dictionary."""
        return CapGain(utility.from_js_date(data['date']), data['symbol'],
                       Decimal(data['amount']), data['longTerm'],
                       data['wasReinvested'])


class Liquidation(Transaction):
    """A security liquidation transaction."""
    def __init__(self, date, description, amount):
        self.date = date
        self.description = description
        self.amount = amount

    def __repr__(self):
        return '%s  %s liquidation of %s' % (self.date,
                                             dollars.to_str(self.amount),
                                             self.description[:30])

    @staticmethod
    def from_decoded_json(data):
        """Creates a Liquidation transaction from a dictionary."""
        return Liquidation(utility.from_js_date(data['date']),
                           data['description'], Decimal(data['amount']))


class Interest(Transaction):
    """An interest deposit transaction."""
    def __init__(self, date, amount):
        self.date = date
        self.amount = amount

    def __repr__(self):
        return '%s  Interest: %s' % (self.date, dollars.to_str(self.amount))

    @staticmethod
    def from_decoded_json(data):
        """Creates an Interest transaction from a dictionary."""
        return Interest(utility.from_js_date(data['date']),
                        Decimal(data['amount']))


class Buy(Transaction):
    """A buy transaction."""
    # pylint: disable=too-many-arguments
    def __init__(self, date, symbol, num_shares, price, fees, total,
                 is_reinvestment):
        self.date = date
        self.symbol = symbol
        self.num_shares = num_shares
        self.price = price
        self.is_reinvestment = is_reinvestment
        self.fees = fees
        self.total = total

    def __repr__(self):
        return '%s  Bought %.2f %s at %s%s - %s fee' % (
            self.date, self.num_shares, self.symbol,
            dollars.to_str(self.price),
            ' (reinvestment)' if self.is_reinvestment else '',
            dollars.to_str(self.fees))

    @staticmethod
    def from_decoded_json(data):
        """Creates a Buy transaction from a dictionary."""
        quantity = Decimal(data['quantity'])
        price = Decimal(data['price'])
        fees = Decimal(data['fees'])
        total = Decimal(data['total'])
        return Buy(utility.from_js_date(data['date']), data['symbol'],
                   quantity, price, fees, total, data['wasReinvestment'])


class Sell(Transaction):
    """A sell transaction."""
    # pylint: disable=too-many-arguments
    def __init__(self, date, symbol, num_shares, price, fees, total):
        self.date = date
        self.symbol = symbol
        self.num_shares = num_shares
        self.price = price
        self.fees = fees
        self.total = total

    def __repr__(self):
        return '%s  Sold %.2f %s at %s - %s fee' % (
            self.date, self.num_shares, self.symbol,
            dollars.to_str(self.price), dollars.to_str(self.fees))

    @staticmethod
    def from_decoded_json(data):
        """Creates a Sell transaction from a dictionary."""
        quantity = Decimal(data['quantity'])
        price = Decimal(data['price'])
        fees = Decimal(data['fees'])
        total = Decimal(data['total'])  # quantity * price - fees
        return Sell(utility.from_js_date(data['date']), data['symbol'],
                    quantity, price, fees, total)


class Transfer(Transaction):
    """A cash transfer transaction."""
    def __init__(self, date, amount):
        self.date = date
        self.amount = amount

    def __repr__(self):
        if self.amount > 0:
            return '%s  Deposited %s' % (
                self.date, dollars.to_str(self.amount))
        return '%s  Withdrew %s' % (self.date, dollars.to_str(self.amount))

    @staticmethod
    def from_decoded_json(data):
        """Creates a Transfer transaction from a dictionary."""
        return Transfer(utility.from_js_date(data['date']),
                        Decimal(data['amount']))


class SecurityTransfer(Transaction):
    """A security transfer transaction."""
    def __init__(self, date, symbol, num_shares):
        self.date = date
        self.symbol = symbol
        self.num_shares = num_shares

    def __repr__(self):
        return '%s  Transferred %.2f %s %s' % (
            self.date, self.num_shares, self.symbol,
            'in' if self.num_shares > 0 else 'out')

    @staticmethod
    def from_decoded_json(data):
        """Creates a SecurityTransfer transaction from a dictionary."""
        return SecurityTransfer(utility.from_js_date(data['date']),
                                data['symbol'], Decimal(data['quantity']))

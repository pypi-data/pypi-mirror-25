#!/usr/bin/env python2

"""
Imports transactions from files.
"""

from decimal import Decimal
import datetime
import string

from stocktracker import dollars, transactions


class Importer(object):
    """Base class for an importer."""

    def __init__(self, filename):
        self.filename = filename
        self.transactions = []

    def do_import(self):
        """Opens the file and delegates the importing."""
        with open(self.filename, 'r') as source:
            self.import_from_file(source)

    def import_from_file(self, source):
        """Imports transactions from the opened file."""
        raise NotImplementedError


class TDAmeritradeImporter(Importer):
    """Imports from CSV files downloaded from tdameritrade.com."""

    _expected_cols = (
        'date', 'transaction id', 'description', 'quantity', 'symbol',
        'price', 'commission', 'amount', 'net cash balance', 'reg fee',
        'short-term rdm fee', 'fund redemption fee', 'deferred sales charge',
    )

    def import_from_file(self, source):
        header_line = source.readline()
        if not header_line:
            raise RuntimeError('File is empty')

        self._verify_header(header_line)

        end_reached = False
        for line in source:
            if end_reached:
                raise RuntimeError('End of file already reached')
            line = line.strip()
            if line == '***END OF FILE***':
                end_reached = True
            else:
                transaction = self._parse_transaction(line)
                if transaction:
                    self.transactions.append(transaction)
        if not end_reached:
            raise RuntimeError('End of file marker not found')

    def _verify_header(self, header):
        header_cols = string.split(header.strip(), ',')
        assert len(self._expected_cols) == len(header_cols), (
            'Unexpected header line: %s' % header)

    def _parse_transaction(self, line):
        cols = [col.strip() for col in string.split(line, ',')]
        assert len(cols) == len(self._expected_cols), (
            'Wrong number of columns in line: %r' % line)

        data = dict()
        for i in xrange(0, len(self._expected_cols)):
            data[self._expected_cols[i]] = cols[i]

        desc = data['description'].lower()

        ignored_prefixes = ('money market purchase', 'money market redemption')
        for prefix in ignored_prefixes:
            if desc.startswith(prefix):
                return None

        # Fix up common columns.
        data['symbol'] = data['symbol'].upper()
        data['date'] = (
            datetime.datetime.strptime(data['date'], '%m/%d/%Y').date())
        if data['quantity']:
            data['quantity'] = Decimal(data['quantity'])
        if data['amount']:
            data['amount'] = Decimal(data['amount'])

        # Map of transaction description prefixes to the parse function to use
        # for that transaction.
        desc_prefixes = {
            'money market interest': self._parse_interest,
            'off-cycle interest': self._parse_interest,
            'bought ': self._parse_buy,
            'sold ': self._parse_sell,
            'qualified dividend ': self._parse_dividend,
            'ordinary dividend ': self._parse_dividend,
            'client requested electronic funding receipt':
            self._parse_deposit,
            'client requested electronic funding disbursement':
            self._parse_withdrawal,
            'transfer of security or option out':
            self._parse_security_transfer,
            'long term gain distribution': self._parse_cap_gain,
        }

        for prefix in desc_prefixes:
            if desc.startswith(prefix):
                return desc_prefixes[prefix](data)

        raise RuntimeError('Unhandled transaction: %r' % line)

    def _parse_interest(self, data):
        if data['description'].lower().startswith('off-cycle interest'):
            amount = data['amount']
        else:
            amount = data['quantity']
        assert amount > 0
        return transactions.Interest(data['date'], amount)

    def _parse_buy(self, data):
        assert data['symbol']
        assert data['quantity'] > 0

        # The total determines our basis, so make sure it accounts for stock
        # price and fees.
        total = -data['amount']
        price = Decimal(data['price'])
        fees = Decimal(data['commission'])
        expected_total = data['quantity'] * price + fees
        assert dollars.round_decimal(total) == (
            dollars.round_decimal(expected_total))

        return transactions.Buy(data['date'], data['symbol'], data['quantity'],
                                price, fees, total, False)

    def _parse_sell(self, data):
        assert data['symbol']
        assert data['quantity'] > 0

        # The total determines our gains, so make sure it accounts for stock
        # price and fees.
        total = data['amount']
        price = Decimal(data['price'])
        fees = Decimal(data['commission']) + Decimal(data['reg fee'])
        expected_total = data['quantity'] * price - fees
        assert dollars.round_decimal(total) == (
            dollars.round_decimal(expected_total))

        return transactions.Sell(data['date'], data['symbol'],
                                 data['quantity'], price, fees, total)

    def _parse_dividend(self, data):
        assert data['symbol']
        assert not data['commission']
        assert not data['reg fee']

        assert data['amount'] > 0
        qualified = data['description'].lower().startswith('qualified')

        return transactions.Dividend(data['date'], data['symbol'],
                                     data['amount'], qualified, False)

    def _parse_cap_gain(self, data):
        assert data['symbol']
        assert not data['commission']
        assert not data['reg fee']

        assert data['amount'] > 0
        long_term = data['description'].lower().startswith('long term')
        assert long_term  # TODO: handle short term

        return transactions.CapGain(data['date'], data['symbol'],
                                    data['amount'], long_term, False)

    def _parse_deposit(self, data):
        assert data['amount'] > 0
        return transactions.Transfer(data['date'], data['amount'])

    def _parse_withdrawal(self, data):
        assert data['amount'] < 0
        return transactions.Transfer(data['date'], data['amount'])

    def _parse_security_transfer(self, data):
        # TODO: Handle transfer in.
        assert data['symbol']
        assert data['quantity'] > 0
        amount_transferred = -data['quantity']
        return transactions.SecurityTransfer(data['date'], data['symbol'],
                                             amount_transferred)

# all_transactions = []
# for i in xrange(2008, 2018):
#     importer = TDAmeritradeImporter('sample_data/td_ameritrade_%d.csv' % i)
#     importer.do_import()
#     all_transactions.extend(importer.transactions)
# for txn in all_transactions:
#     if not isinstance(txn, transactions.Interest) and not isinstance(
#             txn, transactions.Dividend):
#         print txn

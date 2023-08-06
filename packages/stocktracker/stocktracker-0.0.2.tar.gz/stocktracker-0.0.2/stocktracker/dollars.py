#!/usr/bin/env python2

"""
Convenience functions for dollar and decimal conversions.
"""

import decimal
from decimal import Decimal

# Rounds away from 0, enables most traps, prec = 9
decimal.setcontext(decimal.BasicContext)


def round_decimal(value, num_decimal_places=2):
    """Returns the decimal value rounded to num_decimal_places."""
    quantize = Decimal(10) ** -num_decimal_places  # 2 places => '0.01'
    return value.quantize(quantize)


def parse(num):
    """Parses a string number into a decimal.

    Example valid formats:
        Dollar(1)
        Dollar(-12.3456)
        Dollar('1234.56')
        Dollar('1,234.56')
        Dollar('$12.34')
        Dollar('$-12.34')
        Dollar('-$12.34')
        Dollar('($12.34)')
        Dollar('$(12.34)')
    """
    parsed = num.strip().replace(',', '')
    if not parsed:
        return 0
    sign = 1
    while True:
        if parsed[0] == '-':
            parsed = parsed[1:]
            sign *= -1
        elif parsed[0] == '$':
            parsed = parsed[1:]
        elif parsed[0] == '(':
            assert parsed[-1] == ')', 'Unparsable number %s' % num
            parsed = parsed[1:-1]
            sign *= -1
        else:
            break
    return sign * Decimal(parsed)


def remove_trailing_zeros(value):
    """ Returns a Decimal without trailing zeros after the decimal point."""
    decimal_str = str(value)
    dot_index = decimal_str.find('.')
    if dot_index != -1:
        while decimal_str[-1] == '0':
            decimal_str = decimal_str[:-1]
        if decimal_str[-1] == '.':
            decimal_str = decimal_str[:-1]
    return Decimal(decimal_str)


def precise_division(exact_product, other_term, verbose=False):
    """Returns a Decimal with the minimum precision such that the product of the
    return value and other_term can be rounded to exact_product without error.
    """
    product_str = str(exact_product)
    product_str_dot_index = product_str.find('.')
    if product_str_dot_index == -1:
        num_decimals = 0
    else:
        num_decimals = len(product_str) - product_str_dot_index - 1

    if verbose:
        print ('Finding a term that multiplies to %s after rounding to %d '
               'decimal places' %
               (str(exact_product), num_decimals))

    precise = exact_product / other_term
    if verbose:
        print 'Unrounded value is %s' % precise

    assert abs(precise * other_term - exact_product) < .0001

    dot_index = str(precise).find('.')
    if dot_index == -1:
        return precise
    assert dot_index < len(str(precise)) - 1, (
        'Dot apparently can be the last character, so return here too')

    for prec in xrange(0, 20):
        attempt = round_decimal(precise, prec)
        product = attempt * other_term
        rounded_product = round_decimal(product, num_decimals)
        if verbose:
            print 'Trying %s => %s => %s' % (attempt, product, rounded_product)

        if rounded_product == exact_product:
            return attempt
    assert False, 'No value found'


def increment_last_place(value):
    """Increments the last digit of a Decimal, irrespective of sign."""
    d_tuple = value.as_tuple()
    digits = d_tuple.digits

    digit_list = list(digits[:-1] + (digits[-1] + 1,))
    i = len(digit_list) - 1
    while digit_list[i] == 10:
        digit_list[i] = 0
        if i == 0:
            digit_list.insert(0, 1)
            break
        digit_list[i - 1] += 1
        i -= 1

    return Decimal((d_tuple.sign, tuple(digit_list), d_tuple.exponent))


def decrement_last_place(value):
    """Decrements the last digit of a Decimal, irrespective of sign.

    Swaps sign if the input equals 0.
    """
    # todo: test 0 case works for both inc & dec
    if value == 0:
        return -increment_last_place(value)

    d_tuple = value.as_tuple()
    digits = d_tuple.digits

    digit_list = list(digits[:-1] + (digits[-1] - 1,))
    i = len(digit_list) - 1
    while digit_list[i] == -1:
        assert i > 0
        digit_list[i] = 9
        digit_list[i - 1] -= 1
        i -= 1

    return Decimal((d_tuple.sign, tuple(digit_list), d_tuple.exponent))


# TODO: the txt parser should have a param for whether or not to assume
# totals off by more than N have a fee implied that we should calculate
def fix_up_transaction(num_shares, price, total, fees=None):
    """Returns the likely actual values by checking for fees or rounding error.

    We always assume the total is the source of truth for the cash being moved,
    so we adjust the other factors to determine the "real" values used.

    When `fee` is specified, the price is simply adjusted to account for
    rounding error.

    Otherwise, if the difference between `total` and `num_shares * price` is
    greater than any possible rounding error, we assume that difference is the
    fee. When we can attribute the difference to rounding error, we adjust
    `price` to be more precise so we can arrive at the total. (We assume the
    fee is rounded to the nearest penny, so we may adjust `price` anyway if
    there are still fractional pennies left over after determining the fee.

    `num_shares` and `total` are never adjusted.
    """
    assert num_shares > 0
    assert price > 0
    assert total > 0

    assert fees is None or fees >= 0

    result = {'num_shares': num_shares, 'total': total}

    diff = total - num_shares * price - (0 if fees is None else fees)
    if diff == 0:
        result["price"] = price
        result["fees"] = Decimal(0) if fees is None else fees
        return result

    # If fees were specified, the difference must be attributed to price.
    if fees is not None:
        result['price'] = precise_division(total - fees, num_shares)
        result['fees'] = fees
        return result

    # We won't adjust num_shares, but it could have contributed to rounding
    # error.
    num_shares_up = increment_last_place(num_shares)
    num_shares_down = decrement_last_place(num_shares)

    price_up = increment_last_place(price)
    price_down = decrement_last_place(price)

    highest_possible_total = num_shares_up * price_up
    lowest_possible_total = num_shares_down * price_down

    possible_fees = round_decimal(total - num_shares * price)
    if possible_fees <= 0 or (total >= lowest_possible_total and total <=
                              highest_possible_total):
        # Assume the entire difference can be attributed to rounding error.
        result['price'] = precise_division(total, num_shares)
        result['fees'] = Decimal(0)
        return result

    result['price'] = price
    result['fees'] = possible_fees
    return result


def to_str(num):
    """Prints a decimal number as a dollar amount."""
    is_negative = num < 0
    if is_negative:
        return '$(%.2f)' % round_decimal(-num, 2)
    return '$%.2f' % round_decimal(num, 2)

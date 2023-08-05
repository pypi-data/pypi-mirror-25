"""oTree Public API utilities"""

import json
from decimal import Decimal

from django.conf import settings
from django.utils import formats, numberformat
from django.utils.safestring import mark_safe
from django.utils.translation import ungettext

import six

import easymoney


# =============================================================================
# MONKEY PATCH - fix for https://github.com/oTree-org/otree-core/issues/387
# =============================================================================

# Black Magic: The original number format of django used inside templates don't
# work if the currency code contains non-ascii characters. This ugly hack
# remplace the original number format and when you has a easy_money instance
# simple use the old unicode casting.

_original_number_format = numberformat.format


def otree_number_format(number, *args, **kwargs):
    if isinstance(number, easymoney.Money):
        return six.text_type(number)
    return _original_number_format(number, *args, **kwargs)

numberformat.format = otree_number_format


# =============================================================================
# CLASSES
# =============================================================================

class RealWorldCurrency(easymoney.Money):
    '''payment currency'''

    CODE = settings.REAL_WORLD_CURRENCY_CODE
    LOCALE = settings.REAL_WORLD_CURRENCY_LOCALE
    DECIMAL_PLACES = settings.REAL_WORLD_CURRENCY_DECIMAL_PLACES

    def to_number(self):
        '''DEPRECATED. Don't use this.'''
        return Decimal(self)



class Currency(RealWorldCurrency):
    '''game currency'''

    # if I uncomment the below,
    # it should solve the problem in PyCharm where currency amounts are
    # highlighted in yellow if you try to divide
    # by a number. but there are other currency problems, like adding
    # to a number. Or even adding IntegerField to a number.
    # so i want to understand better first how to solve the problem generally
    # def __new__(cls, amount):
    #     return super().__new__(cls, amount)

    if settings.USE_POINTS:
        DECIMAL_PLACES = settings.POINTS_DECIMAL_PLACES

    @classmethod
    def _format_currency(cls, number):
        if settings.USE_POINTS:

            formatted_number = formats.number_format(number)

            if hasattr(settings, 'POINTS_CUSTOM_FORMAT'):
                return settings.POINTS_CUSTOM_FORMAT.format(formatted_number)

            # Translators: display a number of points,
            # like "1 point", "2 points", ...
            # See "Plural-Forms" above for pluralization rules
            # in this language.
            # Explanation at http://bit.ly/1IurMu7
            # In most languages, msgstr[0] is singular,
            # and msgstr[1] is plural
            # the {} represents the number;
            # don't forget to include it in your translation
            return ungettext('{} point', '{} points', number).format(
                formatted_number)
        else:
            return super(Currency, cls)._format_currency(number)

    def to_real_world_currency(self, session):
        if settings.USE_POINTS:
            return RealWorldCurrency(
                float(self) *
                session.config['real_world_currency_per_point'])
        else:
            return self


class _CurrencyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, easymoney.Money):
            if obj.DECIMAL_PLACES == 0:
                return int(obj)
            return float(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def safe_json(obj):
    return mark_safe(json.dumps(obj, cls=_CurrencyEncoder))


def currency_range(first, last, increment):
    assert last >= first
    if Currency(increment) == 0:
        if settings.USE_POINTS:
            setting_name = 'POINTS_DECIMAL_PLACES'
        else:
            setting_name = 'REAL_WORLD_CURRENCY_DECIMAL_PLACES'
        raise ValueError(
            ('currency_range() step argument must not be zero. '
             'Maybe your {} setting is '
             'causing it to be rounded to 0.').format(setting_name)
        )

    assert increment > 0  # not negative

    values = []
    current_value = Currency(first)

    while True:
        if current_value > last:
            return values
        values.append(current_value)
        current_value += increment

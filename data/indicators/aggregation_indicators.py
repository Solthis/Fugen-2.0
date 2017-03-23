# coding: utf-8

from pyparsing import *

from data.indicators.base_indicator import INDICATORS_REGISTRY
from data.indicators import BaseIndicator, IndicatorMeta


class AggregationIndicator(BaseIndicator):
    """
    Base indicator class for indicators made using an aggregation expression
    defined by the user.
    """

    def __init__(self, fuchia_database, aggregation_expression):
        super(AggregationIndicator, self).__init__(fuchia_database)
        self.aggregation_expression = aggregation_expression
        self.aggregated_indicator = self.parse_aggregation_expression(
            self.aggregation_expression
        )

    @classmethod
    def get_key(cls):
        raise NotImplementedError()

    def get_value(self, limit_date, start_date=None, gender=None,
                  age_min=None, age_max=None, age_is_null=False,
                  include_null_dates=False):
        return self.aggregated_indicator.get_value(
            limit_date,
            start_date=start_date,
            gender=gender,
            age_min=age_min,
            age_max=age_max,
            age_is_null=age_is_null,
            include_null_dates=include_null_dates
        )

    def parse_aggregation_expression(self, aggregation_expression):
        """
        This static method takes a aggregation expression, parse it, and if it
        is correct creates a indicator instance corresponding to the operations
        described in the expression.
        :param aggregation_expression: The aggregation expression.
        :return: The indicator obtained after parsing and applying the
        expression.
        """
        raise NotImplementedError()


class ArithmeticAggregationIndicator(AggregationIndicator):

    def parse_aggregation_expression(self, aggregation_expression):
        expr = infixNotation(
            Word(srange("[A-Za-z0-9_]")) | Word(nums),
            [
                (oneOf('-'), 1, opAssoc.RIGHT, nest_operand_pairs),
                (oneOf('* /'), 2, opAssoc.LEFT, nest_operand_pairs),
                (oneOf('+ -'), 2, opAssoc.LEFT, nest_operand_pairs),
            ]
        )
        p = list(expr.scanString(aggregation_expression))
        if len(p) != 1:
            raise ParseException("The aggregation expression is incorrect")
        return self._aggregate_pair(p[0][0][0])

    def _aggregate_pair(self, pair):
        if isinstance(pair, str):
            return self._get_indicator(pair)
        if len(pair) == 2:
            operator = pair[0]
            i1 = self._get_indicator(pair[1])
            if operator == "-":
                return -i1
            else:
                raise ValueError(
                    "'{}' is not a valid arithmetic operator.".format(operator)
                )
        i1 = self._get_indicator(pair[0])
        operator = pair[1]
        i2 = self._get_indicator(pair[2])
        if operator == "+":
            return i1 + i2
        elif operator == "-":
            return i1 - i2
        elif operator == "*":
            return i1 * i2
        elif operator == "/":
            return i1 / i2
        else:
            raise ValueError(
                "'{}' is not a valid arithmetic operator.".format(operator)
            )

    def _get_indicator(self, member):
        if isinstance(member, str):
            return INDICATORS_REGISTRY[member]['class'](self.fuchia_database)
        return self._aggregate_pair(member)

    @classmethod
    def get_key(cls):
        raise NotImplementedError()


class LogicalAggregationIndicator(AggregationIndicator):

    def parse_aggregation_expression(self, aggregation_expression):
        expr = infixNotation(
            Word(srange("[A-Za-z0-9_]")) | Word(nums),
            [
                (oneOf('~'), 1, opAssoc.RIGHT, nest_operand_pairs),
                (oneOf('&'), 2, opAssoc.LEFT, nest_operand_pairs),
                (oneOf('|'), 2, opAssoc.LEFT, nest_operand_pairs),
            ]
        )
        p = list(expr.scanString(aggregation_expression))
        if len(p) != 1:
            raise ParseException("The aggregation expression is incorrect")
        return self._aggregate_pair(p[0][0][0])

    def _aggregate_pair(self, pair):
        if isinstance(pair, str):
            return self._get_indicator(pair)
        if len(pair) == 2:
            operator = pair[0]
            i1 = self._get_indicator(pair[1])
            if operator == "~":
                return ~i1
            else:
                raise ValueError(
                    "'{}' is not a valid logical operator.".format(operator)
                )
        i1 = self._get_indicator(pair[0])
        operator = pair[1]
        i2 = self._get_indicator(pair[2])
        if operator == "&":
            return i1 & i2
        elif operator == "|":
            return i1 | i2
        else:
            raise ValueError(
                "'{}' is not a valid logical operator.".format(operator)
            )

    def _get_indicator(self, member):
        if isinstance(member, str):
            return INDICATORS_REGISTRY[member]['class'](self.fuchia_database)
        return self._aggregate_pair(member)

    @classmethod
    def get_key(cls):
        raise NotImplementedError()


def make_arithmetic_aggregation_indicator(aggregation_expression, key,
                                          overwrite_key=False):
    """
    Generates an ArithmeticAggregationIndicator subclass from an aggregation
    expression and a key.
    :param aggregation_expression:
    :param key
    :return: The generated class.
    """
    # Duplicate keys not allowed
    if key in INDICATORS_REGISTRY:
        # Except if overwrite key is True
        if overwrite_key:
            INDICATORS_REGISTRY.pop(key)
        else:
            raise ValueError("The key '{}' already exists.".format(key))

    # Create the class
    class A(ArithmeticAggregationIndicator):
        """
        Generated ArithmeticAggregationIndicator subclass
        """
        def __init__(self, fuchia_database):
            super(A, self).__init__(
                fuchia_database,
                aggregation_expression
            )

        @classmethod
        def get_key(cls):
            return key
    return A


def make_logical_aggregation_indicator(aggregation_expression, key,
                                       overwrite_key=False):
    """
    Generates an LogicalAggregationIndicator subclass from an aggregation
    expression and a key.
    :param aggregation_expression:
    :param key
    :return: The generated class.
    """
    # Duplicate keys not allowed
    if key in INDICATORS_REGISTRY:
        # Except if overwrite key is True
        if overwrite_key:
            INDICATORS_REGISTRY.pop(key)
        else:
            raise ValueError("The key '{}' already exists.".format(key))

    # Create the class
    class A(LogicalAggregationIndicator):
        """
        Generated LogicalAggregationIndicator subclass
        """
        def __init__(self, fuchia_database):
            super(A, self).__init__(
                fuchia_database,
                aggregation_expression
            )

        @classmethod
        def get_key(cls):
            return key
    return A


def nest_operand_pairs(tokens):
    tokens = tokens[0]
    ret = ParseResults(tokens[:3])
    remaining = iter(tokens[3:])
    done = False
    while not done:
        next_pair = (next(remaining,None), next(remaining,None))
        if next_pair == (None, None):
            done = True
            break
        ret = ParseResults([ret])
        ret += ParseResults(list(next_pair))
    return [ret]

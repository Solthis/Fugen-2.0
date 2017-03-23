# coding: utf-8

from pyparsing import *

from data.indicators.base_indicator import INDICATORS_REGISTRY
from data.indicators import BaseIndicator


class AggregationIndicator(BaseIndicator):
    """
    Base indicator class for indicators made using an aggregation expression
    defined by the user.
    """

    @classmethod
    def get_key(cls):
        raise NotImplementedError()

    def __init__(self, fuchia_database, aggregation_expression):
        super(AggregationIndicator, self).__init__(fuchia_database)
        self.aggregation_expression = aggregation_expression
        self.aggregated_indicator = self.parse_aggregation_expression(
            self.aggregation_expression
        )

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
                (oneOf('* /'), 2, opAssoc.LEFT, nest_operand_pairs),
                (oneOf('+ -'), 2, opAssoc.LEFT, nest_operand_pairs),
            ]
        )
        p = list(expr.scanString(aggregation_expression))
        if len(p) != 1:
            raise ParseException("The aggregation expression is incorrect")
        return self._aggregate_pair(p[0][0][0])

    def _aggregate_pair(self, pair):
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
        pass


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

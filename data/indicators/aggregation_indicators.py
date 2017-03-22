# coding: utf-8

from pyparsing import *

from data.indicators.base_indicator import INDICATORS_REGISTRY
from data.indicators import PatientIndicator


class AggregationIndicator(PatientIndicator):
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
        print(pair)
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

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        pass

    def under_arv(self):
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

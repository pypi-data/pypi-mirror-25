"""
Relevance facets module.

This module provides the interface definitions for defining facets.
"""

import abc
import dateutil.parser
from dateutil.relativedelta import relativedelta


class FacetDefinitionError(TypeError):
    """
    Exception class when a facet is not defined properly.
    """
    def __init__(self, name: str, msg: str):
        """
        Initialize the exception.

        :param name: the name of the facet that caused the error.
        :param msg: the error message.
        """
        super().__init__('{0}: {1}'.format(name, msg))
        self.name = name


class FacetValueError(ValueError, RuntimeError):
    """
    Exception class when a supplied facet value is invalid.
    """
    def __init__(self, name: str, value: str):
        """
        Initialize the exception.

        :param name: the name of the facet that caused the error.
        :param value: the value of the facet that caused the error.
        """
        super().__init__('unknown value "{0}" for facet "{1}"'.format(value, name))
        self.name = name
        self.value = value


class FacetNotDefinedError(NameError, RuntimeError):
    """
    Exception class for undefined facets.
    """
    def __init__(self, name: str):
        """
        Initialize the exception.

        :param name: the name of the facet that caused the error.
        """
        super().__init__('the facet "{0}" is not defined'.format(name))
        self.name = name


class Facet(object, metaclass=abc.ABCMeta):
    """
    Facet definition class.

    This class is used to define facets within an engine.
    """
    def __init__(self, *, field: str=None, path: str=None):
        """
        Initialize the definition.

        :param field: the field for the facet. Mutually exclusive with path.
        :param path: the path or the facet. Mutually exclusive with field.
        :param facet_type: the type of facet to define.
        """
        if field is not None and path is not None:
            raise FacetDefinitionError(None, 'field and path are mutually exclusive')

        self.field = field
        self.path = path


class TermFacet(Facet):
    """
    Facet type for term facets.

    Aggregates on matching terms.
    """
    pass


class HistogramFacet(Facet):
    """
    Facet type for histogram facets.

    Facets that use ranges should inherit from this abstract class.
    """
    @abc.abstractmethod
    def get_range_for(self, value: object) -> tuple:
        """
        Get a start and end range given a specific value.

        :param value: the value to get the range for.
        :returns: a tuple containing the start and end values for the range.
        """
        pass


class DateFacet(HistogramFacet):
    """
    Facet type for date/time histogram facets.

    Aggregates on date intervals.
    """
    # Interval definitions
    YEAR = 'year'
    QUARTER = 'quarter'
    MONTH = 'month'
    WEEK = 'week'
    DAY = 'day'
    HOUR = 'hour'
    MINUTE = 'minute'
    SECOND = 'second'

    def __init__(self, *args, interval: str=MONTH, **kwargs):
        """
        Initialize the facet.

        :param interval: the interval at which to group the results: year, quarter, month,
        week, day, hour, minute, second.
        """
        super().__init__(*args, **kwargs)
        self.interval = interval

    def get_range_for(self, value: int) -> tuple:
        """
        Override abstract method.
        """
        start = dateutil.parser.parse(value)
        prop, delta = self.interval, 1

        if self.interval == DateFacet.YEAR:
            if start.month != 1 or start.day != 1 or start.hour != 0 or \
               start.minute != 0 or start.second != 0:
                raise FacetValueError(self, value)

        if self.interval == DateFacet.QUARTER:
            if start.month not in [1, 4, 7, 10] or start.day != 1 or \
               start.hour != 0 or start.minute != 0 or start.second != 0:
                raise FacetValueError(self, value)
            prop, delta = 'month', 3

        if self.interval == DateFacet.MONTH:
            if start.day != 1 or start.hour != 0 or \
               start.minute != 0 or start.second != 0:
                raise FacetValueError(self, value)

        if self.interval == DateFacet.WEEK:
            if start.weekday() != 0:
                raise FacetValueError(self, value)
            prop, delta = 'day', 7

        if self.interval == DateFacet.DAY:
            if start.hour != 0 or start.minute != 0 or start.second != 0:
                raise FacetValueError(self, value)

        if self.interval == DateFacet.HOUR:
            if start.minute != 0 or start.second != 0:
                raise FacetValueError(self, value)

        if self.interval == DateFacet.MINUTE:
            if start.second != 0:
                raise FacetValueError(self, value)

        end = start + relativedelta(**{'{0}s'.format(prop): delta})

        return start.isoformat(), end.isoformat()


class IntervalFacet(HistogramFacet):
    """
    Facet type for histogram facets.

    Aggregates on numeric intervals.
    """
    def __init__(self, *args, interval: int, **kwargs):
        """
        Initialize the facet.

        :param interval: the interval at which to group the results.
        """
        super().__init__(*args, **kwargs)
        self.interval = interval

    def get_range_for(self, value: int) -> tuple:
        """
        Override abstract method.
        """
        if (value % self.interval) > 0:
            raise FacetValueError(self, value)

        return value, value + self.interval


class RangeFacet(HistogramFacet):
    """
    Facet type for rangeed histogram facets.

    Aggregates on specific numeric intervals.
    """
    def __init__(self, *args, ranges: dict, **kwargs):
        """
        Initialize the facet.

        :param interval: the interval at which to group the results.
        """
        super().__init__(*args, **kwargs)
        self.ranges = ranges

    def get_range_for(self, value: int) -> tuple:
        """
        Override abstract method.
        """
        try:
            start, end = self.ranges[value]
        except KeyError:
            raise FacetValueError(self, value)

        return start, end

# coding: utf-8
from pypika import terms, VerticaQuery

from fireant.database import Database
from fireant.slicer import DatetimeInterval


class Trunc(terms.Function):
    """
    Wrapper for Vertica TRUNC function for truncating dates.
    """

    def __init__(self, field, date_format, alias=None):
        super(Trunc, self).__init__('TRUNC', field, date_format, alias=alias)


class Interval(terms.Interval):
    """
    Wrapper for Vertica INTERVAL term.
    """

    def get_sql(self, **kwargs):
        if hasattr(self, 'quarters'):
            expr = getattr(self, 'quarters')
            unit = 'QUARTER'

        elif hasattr(self, 'weeks'):
            expr = getattr(self, 'weeks')
            unit = 'WEEK'

        else:
            # Create the whole expression but trim out the unnecessary fields
            expr = self.trim_pattern.sub(
                '',
                "{years}-{months}-{days} {hours}:{minutes}:{seconds}.{microseconds}".format(
                    years=getattr(self, 'years', 0),
                    months=getattr(self, 'months', 0),
                    days=getattr(self, 'days', 0),
                    hours=getattr(self, 'hours', 0),
                    minutes=getattr(self, 'minutes', 0),
                    seconds=getattr(self, 'seconds', 0),
                    microseconds=getattr(self, 'microseconds', 0),
                )
            )
            unit = '{largest}_{smallest}'.format(
                largest=self.largest,
                smallest=self.smallest,
            ) if self.largest != self.smallest else self.largest

        if unit in ['YEAR']:
            query = 'INTERVAL \'{expr}\' {unit}'
        else:
            # This has day as its maximum interval granularity, so it does not take into account leap years.
            query = 'INTERVAL \'{expr} {unit}\''

        return query.format(expr=expr,  unit=unit)


class VerticaDatabase(Database):
    """
    Vertica client that uses the vertica_python driver.
    """
    # The pypika query class to use for constructing queries
    query_cls = VerticaQuery

    def __init__(self, host='localhost', port=5433, database='vertica',
                 user='vertica', password=None,
                 read_timeout=None):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.read_timeout = read_timeout

    def connect(self):
        import vertica_python

        return vertica_python.connect(
            host=self.host, port=self.port, database=self.database,
            user=self.user, password=self.password,
            read_timeout=self.read_timeout,
        )

    def trunc_date(self, field, interval):
        datetime_intervals = {
            'hour': DatetimeInterval('HH'),
            'day': DatetimeInterval('DD'),
            'week': DatetimeInterval('IW'),
            'month': DatetimeInterval('MM'),
            'quarter': DatetimeInterval('Q'),
            'year': DatetimeInterval('Y')
        }

        interval = datetime_intervals[interval]
        return Trunc(field, interval.size)

    def interval(self, **kwargs):
        return Interval(**kwargs)


def Vertica(*args, **kwargs):
    from warnings import warn
    warn('The Vertica class is now deprecated. Please use VerticaDatabase instead!')
    return VerticaDatabase(*args, **kwargs)

from datetime import date, datetime, timedelta


class DateInterval:
    """
    Represents a date interval


    Attributes
    ----------
    start_date: date
    end_date: date

    """

    def __init__(self, start_date, end_date, fmt='%Y-%m-%d'):
        """
        Instance initializer

        Receives two dates as parameters and creates the interval.
        The date represented by start_date must be earlier than end_date

        Parameters
        ----------
        start_date: date or str
        end_date: date or str
        fmt: str
            Format string for conversion to date
        """

        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, fmt).date()

        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, fmt).date()

        assert isinstance(start_date, date)
        assert isinstance(end_date, date)

        assert start_date < end_date, "start_date > end_date"

        self.__start_date = start_date
        self.__end_date = end_date

    @property
    def start_date(self):
        """
        Getter for start_date

        Returns
        -------
        date
        """
        return self.__start_date

    @property
    def end_date(self):
        """
        Getter for end_date

        Returns
        -------
        date
        """
        return self.__end_date

    def days_between(self, lclose=True, rclose=True):
        """
        Count the number of days between the start_date and end_date

        Parameters
        ----------
        lclose: bool
            If True include start_date in the count
        rclose: bool
            If True include end_date in the count

        Returns
        -------
        int
        """

        n_days = (self.end_date - self.start_date).days

        if not lclose:
            n_days -= 1
        if rclose:
            n_days += 1

        return n_days


def get_last_friday(day=None):
    """
    Get last friday in reference of the day passed as parameter

    Parameters
    ----------
    day: datetime.date
    Returns
    -------
    datetime.date
    """

    if day is None:
        day = date.today()
    days_to_subtract = day.weekday() + 3
    if days_to_subtract > 7:
        days_to_subtract -= 7
    last_friday = day - timedelta(days=days_to_subtract)
    return last_friday

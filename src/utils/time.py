import itertools

from abc import ABC
from datetime import datetime
from enum import Enum
from math import ceil
from typing import Tuple

from .errors import DateError


def is_leap_year(year: int) -> bool:
    return year % 4 == 0 and (not year % 100 == 0 or year % 400 == 0)


def days_in_month(month: int, year: int):
    month_year = (month, year)

    match month_year:
        case (2, y) if is_leap_year(y):
            return 29
        case (2, _):
            return 28
        case (m, _) if m in [4, 6, 9, 11]:
            return 30
        case (m, _) if m in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        case (m, _) if m > 12:
            raise DateError(
                f"Invalid value {m} passed for month"
                "The month argument should only be assigned integer values from 1 to 12."
            )
        case _:
            raise DateError("Invalid input.")


class DayOfWeekResolver:
    def __init__(self, month: int, year: int, day: int):
        self.month = month
        self.year = year
        self.day = day
        self.date = datetime(year=year, month=month, day=day)
        self.day_of_week = self.date.weekday()

    def is_weekday(self) -> bool:
        return self.day_of_week < 5

    def weekdays_remaining(self):
        if not self.is_weekday():
            return 0
        return 4 - self.day_of_week

    def days_to_previous_weekday(self):
        if self.is_weekday():
            return 0
        return self.day_of_week - 4

    def days_to_next_weekday(self):
        if self.is_weekday():
            return 0
        return 7 - self.day_of_week


class DayOfMonthResolver:
    def __init__(self, month: int, year: int):
        self.month = month
        self.year = year
        self.days_in_month = days_in_month(self.month, self.year)

    def first_day(self, weekday=True) -> int:
        if weekday:
            return self.weekday_after(1)
        return 1

    def last_day(self, weekday=True) -> int:
        if weekday:
            return self.weekday_before(self.days_in_month)
        return self.days_in_month

    def weekday_before(self, day: int) -> int:
        """
        If the day is a Saturday or a Sunday, return the day of the month corresponding to Friday of that week.
        Otherwise, return the given day. This method should only be used for days which occur later in the month.
        """
        if day > self.days_in_month:
            raise DateError(
                f"The value day={day} is out of range."
                f"There are only {self.days_in_month} for month = {self.month}"
            )

        resolver = DayOfWeekResolver(year=self.year, month=self.month, day=day)
        weekday = day - resolver.days_to_previous_weekday()

        if weekday <= 0:
            print(
                "Warning:  The previous weekday is not contained in the given month."
                "The method 'weekday_before' should only be used for day which occur late in the month'"
                "Use the method 'weekday_after' for days which occur towards the beginning of a month."
            )
            return 0

        return weekday

    def weekday_after(self, day: int) -> int:
        """
        If the day is a Saturday or a Sunday, return the day of the month corresponding to Monday of the next week.
        Otherwise, return the given day. This method should only be used for days which occur earlier in the month.
        """
        if day > self.days_in_month:
            raise DateError(
                f"The value day={day} is out of range."
                f"There are only {self.days_in_month} for month = {self.month}"
            )

        resolver = DayOfWeekResolver(year=self.year, month=self.month, day=day)
        weekday = day + resolver.days_to_next_weekday()

        if weekday > self.days_in_month:
            print(
                "Warning:  The next weekday is not contained in the given month."
                "The method 'weekday_after' should only be used for day which occur early in the month'"
                "Use the method 'weekday_before' for days which occur towards the end of a month."
            )
            return 0

        return weekday

    def weekdays(self, start=None, end=None):
        if start is None:
            start = 1
        if end is None:
            end = self.days_in_month
        if start not in range(1, self.days_in_month + 1) or end not in range(1, self.days_in_month + 1):
            raise DateError("Invalid date range.")
        if start > end:
            raise DateError("The end date must be greater than the start date.")

        for day in range(start, end):
            resolver = DayOfWeekResolver(year=self.year, month=self.month, day=day)
            if resolver.is_weekday():
                yield day


class QuarterToDateResolver:
    def __init__(self, year: int, quarter: int):
        self.year = year
        self.quarter = quarter
        self.months = [quarter * 3 - 2 + k for k in range(0, 3)]

    def first_date(self) -> (int, int):
        return self.months[0], DayOfMonthResolver(year=self.year, month=self.months[0]).first_day()

    def last_date(self) -> (int, int):
        return self.months[2], DayOfMonthResolver(year=self.year, month=self.months[2]).last_day()

    @property
    def weekdays(self):
        for month in self.months:
            for day in DayOfMonthResolver(year=self.year, month=month).weekdays():
                yield month, day


class MonthToQuarterResolver:
    def __init__(self, month: int):
        self.month = month
        self._quarter = ceil(self.month / 3)

    @property
    def quarter(self):
        return self._quarter
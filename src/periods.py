from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass, field

from utils.time import DayOfMonthResolver, QuarterToDateResolver, MonthToQuarterResolver, DayOfWeekResolver
from utils.validators import are_instances


class BoundaryState(Enum):
    START = 1
    END = 2
    MIDDLE = 3


@dataclass
class FilingDate(ABC):
    year: int | None = field(default=None)
    quarter: int | None = field(default=None)
    month: int | None = field(default=None)
    day: int | None = field(default=None)
    boundary: BoundaryState | None = field(default=None)
    minYear: int = field(default=2014, init=False)
    errors: list[dict] = field(default_factory=list, init=False)

    def __post_init__(self):
        if self.year is not None and self.year < self.minYear:
            self.errors.append(
                {'Range Error': 'The given year is earlier than the minimum year for the requested form type.'}
            )

    @classmethod
    def from_str(cls, date_str: str, boundary=BoundaryState.MIDDLE) -> object:
        if len(date_str) != 8:
            raise Exception('')
        year = int(date_str[0:4])
        month = int(date_str[4:6])
        day = int(date_str[6:8])
        quarter = MonthToQuarterResolver(month=month).quarter

        return cls(year=year, month=month, day=day, quarter=quarter, boundary=boundary)

    def date_str_formatted(self, sep=''):
        month_str = f"0{self.month}" if self.month < 10 else f"{self.month}"
        day_str = f"0{self.day}" if self.day < 10 else f"{self.day}"
        return sep.join([str(self.year), month_str, day_str])

    @property
    def date_str(self):
        return self.date_str_formatted()

    @property
    def quarter_str(self):
        return f"QTR{self.quarter}"

    @property
    def is_valid(self):
        return not self.errors


@dataclass
class GenericFilingDate(FilingDate):
    pass


@dataclass
class QuarterFilingDate(FilingDate):
    def __post_init__(self):
        super().__post_init__()
        if not self.is_valid:
            return

        match self:
            case QuarterFilingDate(
                year=y,
                quarter=q,
                month=m,
                day=d,
                boundary=BoundaryState.MIDDLE
            ) if q in range(1, 5):
                resolver = DayOfWeekResolver(year=y, month=m, day=d)
                if not resolver.is_weekday():
                    self.errors.append({'Date Error': 'The given date is not a weekday.'})
            case QuarterFilingDate(
                year=y,
                quarter=q,
                boundary=bs
            ) if q in range(1, 5) and bs in [BoundaryState.START, BoundaryState.END]:
                resolver = QuarterToDateResolver(year=y, quarter=q)
                self.month, self.day = resolver.first_date() if bs == BoundaryState.START else resolver.last_date()
            case _:
                self.errors.append({'Argument Error': 'Invalid input arguments.'})


@dataclass
class MonthFilingDate(FilingDate):
    def __post_init__(self):
        super().__post_init__()
        if not self.is_valid:
            return

        match self:
            case MonthFilingDate(
                year=y,
                quarter=q,
                month=m,
                day=d,
                boundary=BoundaryState.MIDDLE,
            ):
                resolver = DayOfWeekResolver(year=y, month=m, day=d)
                if not resolver.is_weekday():
                    self.errors.append({'Date Error': 'The given date is not a weekday.'})
            case MonthFilingDate(year=y, month=m, boundary=bs) if bs in [BoundaryState.START, BoundaryState.END]:
                resolver = DayOfMonthResolver(year=y, month=m)
                self.day = resolver.first_day() if bs == BoundaryState.START else resolver.last_day()
            case _:
                self.errors.append({'Argument Error': 'Invalid input arguments.'})


@dataclass
class FilingPeriod(ABC):
    start: FilingDate
    end: FilingDate
    dates: list[FilingDate] = field(default_factory=list)
    errors: list[dict] = field(default_factory=list, init=False)

    def __post_init__(self):
        if not self.start.is_valid or not self.end.is_valid:
            self.errors.extend(self.start.errors)
            self.errors.extend(self.end.errors)

    @property
    def is_valid(self):
        return not self.errors


@dataclass
class FilingQuarter(FilingPeriod):
    def __post_init__(self):
        super().__post_init__()

        if not self.is_valid:
            return

        if not isinstance(self.start, QuarterFilingDate) or not isinstance(self.end, QuarterFilingDate):
            self.errors.append({
                'Type Error': 'Invalid filing date object passed.'
            })

        self._build_date_list()

    def _build_date_list(self):
        assert self.start.quarter == self.end.quarter and self.start.year == self.end.year

        year = self.start.year
        quarter = self.start.quarter

        resolver = QuarterToDateResolver(year=self.start.year, quarter=self.start.quarter)
        first_month, first_day = resolver.first_date()
        last_month, last_day = resolver.last_date()

        self.dates.append(self.start)
        for month, day in resolver.weekdays:
            if month == first_month and day == first_day:
                continue
            if month == last_month and day == last_day:
                continue

            date = QuarterFilingDate(year=year, quarter=quarter, month=month, day=day, boundary=BoundaryState.MIDDLE)

            if not date.is_valid:
                # print(date.errors)
                continue

            self.dates.append(date)

        self.dates.append(self.end)


def filing_quarter(year: int, quarter: int):
    return FilingQuarter(
        start=QuarterFilingDate(year=year, quarter=quarter, boundary=BoundaryState.START),
        end=QuarterFilingDate(year=year, quarter=quarter, boundary=BoundaryState.END)
    )


@dataclass
class FilingMonth(FilingPeriod):
    def __post_init__(self):
        super().__post_init__()

    def _build_list(self):
        assert self.start.year == self.end.year and self.start.month == self.end.month

        year = self.start.year
        month = self.start.month
        quarter = MonthToQuarterResolver(month=month).quarter
        resolver = DayOfMonthResolver(year=year, month=month)

        for day in resolver.weekdays(start=self.start.day + 1, end=self.end.day - 1):

            date = MonthFilingDate(year=year, quarter=quarter, month=month, day=day, boundary=BoundaryState.MIDDLE)

            if not date.is_valid:
                continue

            self.dates.append(date)

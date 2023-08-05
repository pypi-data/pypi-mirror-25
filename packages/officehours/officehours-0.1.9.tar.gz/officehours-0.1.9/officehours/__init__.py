#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from datetime import date
from datetime import datetime
from datetime import timedelta


__author__ = 'Guillermo Guirao Aguilar'
__email__ = 'contact@guillermoguiraoaguilar.com'
__version__ = '0.1.9'


class TimeFormatError(Exception):
    """ Exception returned when a time string doesn't have the right format """


class Calculator:
    def __init__(self, start='9:00', close='17:00', holidays=None):
        """ Initialize the class

        :param str start: office opening time
        :param str close: office closing time
        :param list holidays: array of bank holidays
        """
        self.start = self.seconds(start)
        self.close = self.seconds(close)
        self.one_day = timedelta(days=1)
        self.holidays = set([self.date(day) for day in holidays or []])

    def set_time(self, date, time):
        """ Returns a datetime object with the date from the first parameter
        and the time from the second. The time can be given as a string or
        taken from another datetime object

        :param datetime date: object containing the date (year, month and day)
        :param str time: time to be set. E.g. '9:00'
        """
        seconds = self.seconds(time)
        hour = int(seconds / 3600)
        minute = int((seconds % 3600) / 60)
        second = int((seconds % 3600) % 60)
        return datetime(date.year, date.month, date.day, hour, minute, second)

    def add_holidays(self, day):
        """ Adds one or more datetime objects to a list of bank holidays

        :param datetime date day: holiday dates
        """
        self.holidays.add(self.date(day))

    def seconds(self, time):
        """ Converts a time to seconds. The time can be provided as the number
        of seconds since the beginning of the day; a string representing a time
        (e.g. '12:30') or a datetime or date object.

        :param str int datetime time: time string in HH:MM format
        """
        if isinstance(time, (int, float)):
            return time
        elif isinstance(time, str):
            hours, minutes = self.validate(time)
            return (int(hours) * 3600) + (int(minutes) * 60)
        elif isinstance(time, datetime):
            return (time.hour * 3600) + (time.minute * 60) + time.second
        elif isinstance(time, date):
            return 0
        else:
            raise TypeError('{} is not a valid time'.format(type(time)))

    @staticmethod
    def validate(time):
        """ Checks whether the string format is correct and returns it as a
        tuple of int

        :param str time: time string in HH:MM format
        """
        if re.match('^\d?\d:\d\d$', time):
            hours, minutes = [int(n) for n in time.split(':')]
            if 0 <= hours < 24 and 0 <= minutes < 60:
                return hours, minutes
        raise TimeFormatError('{} is not a valid time format'.format(time))

    @property
    def work_day(self):
        """ Returns the amount of working seconds per day """
        return self.close - self.start

    @staticmethod
    def date(day):
        """ Ensures that `day` is an instance of datetime.date """
        if isinstance(day, datetime):
            return day.date()
        elif isinstance(day, date):
            return day
        else:
            raise TypeError("{} is not a datetime object".format(type(day)))

    @staticmethod
    def is_weekend(day):
        """ Returns True if `day` is a weekend day

        :param datetime.date day: date
        """
        return day.isoweekday() in [6, 7]

    def is_holiday(self, day):
        """ Returns True if `day` is a bank holiday

        :param datetime.date day: date
        """
        return self.date(day) in self.holidays

    def is_working_day(self, day):
        """ Returns True if `day` is a working day

        :param datetime.date day: date
        """
        return not (self.is_weekend(day) or self.is_holiday(day))

    def is_working_time(self, day):
        """ Returns True if `day` is working time

        :param datetime day: datetime
        """
        if self.is_working_day(day):
            if self.start <= self.seconds(day) <= self.close:
                return True
        return False

    def normalize(self, time):
        """ If `time` is out of office hours, returns
        the closest working time. Do nothing otherwise

        :param int time: time in seconds
        """
        time = self.seconds(time)
        if time < self.start:
            return self.start
        elif time > self.close:
            return self.close
        else:
            return time

    def count(self, from_time, to_time):
        """ Returns the number of hours elapsed between two times.
        Dates are not relevant

        :param datetime from_time: initial datetime
        :param datetime to_time: final datetime
        """
        return self.normalize(to_time) - self.normalize(from_time)

    def previous_office_close(self, day):
        """ Returns a datetime object corresponding to the office closing time
        of the previous working day

        :param datetime day: datetime
        """
        if self.is_working_day(day) and self.seconds(day) > self.close:
            return self.set_time(day, self.close)
        else:
            day -= self.one_day
            while not self.is_working_day(day):
                day -= self.one_day
            return self.set_time(day, self.close)

    def next_office_open(self, day):
        """ Returns a datetime object corresponding to the office opening time
        of the next working day

        :param datetime day: datetime
        """
        if self.is_working_day(day) and self.seconds(day) < self.start:
            return self.set_time(day, self.start)
        else:
            day += self.one_day
            while not self.is_working_day(day):
                day += self.one_day
            return self.set_time(day, self.start)

    def working_days(self, from_date, to_date=None):
        """ Returns the number of working days between two dates

        :param datetime from_date: initial date
        :param datetime to_date: final date. Defaults to current time
        """
        from_date = self.date(from_date)
        to_date = self.date(to_date or datetime.today())
        days = 0
        while from_date < to_date:
            if self.is_working_day(from_date):
                days += 1
            from_date += self.one_day
        return days

    def working_seconds(self, from_time, to_time=None):
        """ Returns the number of working seconds between two dates

        :param datetime from_time: initial date
        :param datetime to_time: final date. Defaults to current time
        """
        if not to_time:
            to_time = datetime.today()
        from_date = self.date(from_time)
        to_date = self.date(to_time)
        if from_date == to_date and self.is_working_day(from_date):
            return max(self.count(from_time, to_time), 0)
        elif from_date < to_date:
            seconds = 0
            if self.is_working_time(from_time):
                seconds += self.count(from_time, self.close)
            from_time = self.next_office_open(from_time)
            while self.date(from_time) < self.date(to_time):
                seconds += self.work_day
                from_time = self.next_office_open(from_time)
            if self.is_working_day(to_time):
                seconds += self.count(self.start, to_time)
            return seconds
        return 0

    def working_hours(self, from_time, to_time=None):
        """ Returns the number of working hours between two dates

        :param datetime from_time: initial date
        :param datetime to_time: final date. Defaults to current time
        """
        return self.working_seconds(from_time, to_time) / 3600.0

    def due_date(self, hours, from_time=None):
        """ Calculates the resulting datetime after a given number of working hours

        :param float hours: amount of working hours
        :param datetime from_time: date from which the hours start
            counting. Defaults to the current datetime
        """
        if not self.is_working_time(from_time):
            from_time = self.next_office_open(from_time or datetime.today())
        remaining = self.count(from_time, self.close)
        seconds = hours * 3600
        if seconds > remaining:
            while seconds > 0:
                if seconds > self.work_day:
                    seconds -= self.work_day
                elif remaining <= seconds <= self.work_day:
                    seconds -= self.work_day
                else:
                    break
                from_time += self.one_day
                while not self.is_working_day(from_time):
                    from_time += self.one_day

        return from_time + timedelta(seconds=seconds)

    def start_time(self, hours, deadline=None):
        """ Calculates the starting datetime required to meet a deadline

        :param float hours: amount of working hours
        :param datetime deadline: datetime by which all working hours
            must have been elapsed. Defaults to the current datetime
        """
        if not self.is_working_time(deadline):
            deadline = self.previous_office_close(deadline or datetime.today())
        remaining = self.count(self.start, deadline)
        seconds = hours * 3600
        if seconds > remaining:
            while seconds > 0:
                if seconds > self.work_day:
                    seconds -= self.work_day
                elif remaining <= seconds <= self.work_day:
                    seconds -= self.work_day
                else:
                    break
                deadline -= self.one_day
                while not self.is_working_day(deadline):
                    deadline -= self.one_day

        return deadline - timedelta(seconds=seconds)

    def find_date(self, hours, from_time=None):
        """ Same as calculating the due date, but accepts a negative number of
        working hours, in which case the start time is calculated instead

        :param float hours: amount of working hours
        :param datetime from_time: date from which the hours start
            counting. Defaults to the current datetime
        """
        if hours >= 0:
            return self.due_date(hours, from_time)
        elif hours < 0:
            return self.start_time(-hours, from_time)

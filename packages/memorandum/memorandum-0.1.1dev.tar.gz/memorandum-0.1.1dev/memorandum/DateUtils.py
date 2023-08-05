###
# Author: Vincent Lucas <vincent.lucas@gmail.com>
###

import calendar
import datetime
import re
from dateutil import tz

class DateUtils(object):

    ###
    # @param day The requested day with format: "yyyymmdd".
    ###
    def get_datetime(
            string):

            fmt = None
            if(re.fullmatch("^\d{8}$", string)):
                fmt = "%Y%m%d"
            elif(re.fullmatch("^\d{8}T\d{6}$", string)):
                fmt = "%Y%m%dT%H%M%S"
            elif(re.fullmatch("^\d{8}T\d{6}Z$", string)):
                fmt = "%Y%m%dT%H%M%SZ"

            if(fmt):
                res = datetime.datetime.strptime(string, fmt)
                return res.replace(tzinfo=tz.tzlocal())

            return None

    def get_date_string(
            date):
        return date.strftime("%Y%m%d")

    def get_caldav_string(
            date):
        return date.strftime("%Y%m%dT%H%M%SZ")

    def get_day_start(
            nb_days_from_day = 0,
            day = None):

        if(day == None):
            day = datetime.date.today()
        day = datetime.datetime.combine(day, datetime.time(0, 0, 0))
        return day.replace(day=day.day + nb_days_from_day)

    def get_day_end(
            nb_days_from_day = 0,
            day = None):

        if(day == None):
            day = datetime.date.today()
        day = datetime.datetime.combine(day, datetime.time(23, 59, 59))
        return day.replace(day=day.day + nb_days_from_day)

    def get_weekday_start(
            day = None):

        if(day == None):
            day = datetime.date.today()
        delta = datetime.timedelta(days=-day.weekday())
        day = day + delta
        day = datetime.datetime.combine(day, datetime.time(0, 0, 0))
        day = day.replace(tzinfo=tz.tzlocal())
        return day

    def get_weekday_end(
            day = None):

        if(day == None):
            day = datetime.date.today()
        day = DateUtils.get_weekday_start(day)
        delta = datetime.timedelta(days=+6)
        day = day + delta
        day = datetime.datetime.combine(day, datetime.time(23, 59, 59))
        day = day.replace(tzinfo=tz.tzlocal())
        return day

    def get_monthday_start(
            day = None):

        if(day == None):
            day = datetime.date.today()
        day = day.replace(day=1)
        day = datetime.datetime.combine(day, datetime.time(0, 0, 0))
        day = day.replace(tzinfo=tz.tzlocal())
        return day

    def get_monthday_end(
            day = None):

        if(day == None):
            day = datetime.date.today()
        max_month_day = calendar.monthrange(day.year, day.month)[1]
        day = day.replace(day=max_month_day)
        day = datetime.datetime.combine(day, datetime.time(23, 59, 59))
        day = day.replace(tzinfo=tz.tzlocal())
        return day

    def to_datetime(
            date):
        if(date == None):
            date = datetime.date.today()
        if(type(date) == datetime.date):
            date = datetime.datetime.combine(date, datetime.time(0, 0, 0))
            date = date.replace(tzinfo=tz.tzlocal())

        return date

###
# Author: Vincent Lucas <vincent.lucas@gmail.com>
###

import sys
import os.path

from .Config import Config
from .VEvent import VEvent
from .CalendarCmds import CalendarCmds
from .DateUtils import DateUtils

import argparse

def cmds():
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "-a",
            "--all",
            help="display all events",
            action="store_true")
    parser.add_argument(
            "-c",
            "--create",
            help="create an event",
            action="store_true")
    parser.add_argument(
            "-d",
            "--date",
            help="the date to display: e.g. 20170831. Today if not defined",
            type=str)
    parser.add_argument(
            "-m",
            "--month",
            help="display month events",
            action="store_true")
    parser.add_argument(
            "-w",
            "--week",
            help="display week events",
            action="store_true")
    args = parser.parse_args()

    # Load the configuration and configure the CalDav session.
    config = Config()

    calendarCmds = CalendarCmds(config.conf)
    events = None

    # create event
    if(args.create):
        print("Create event:\n")
        summary = input('Summary: ')
        location = input('Location: ')
        if(not args.date):
            args.date = input('Date (YYYYMMDD): ')
        start_time = input('Start time (HHMM): ')
        end_time = input('End time (HHMM): ')

        start_date = DateUtils.get_datetime(
                "{0}T{1}00Z".format(args.date, start_time))
        end_date = DateUtils.get_datetime(
                "{0}T{1}00Z".format(args.date, end_time))
        # Create one event
        uid = calendarCmds.create_event(
                summary,
                start_date,
                end_date,
                location=location)
        if(not uid):
            print("Create event: failed\n")
    # Else display events
    else:
        if(args.all):
            print("All events:\n")
            events = calendarCmds.get_events(None, None)
        elif(args.week):
            print("Week events:\n")
            events = calendarCmds.get_events_week(args.date)
        elif(args.month):
            print("Month events:\n")
            events = calendarCmds.get_events_month(args.date)
        else:
            print("Today events:\n")
            events = calendarCmds.get_events_day(args.date)

        for event in events:
            print("{0}\n----".format(event.get_short_str()))
            #print("{0}\n----".format(event.get_long_str()))
            #print("{0}\n----".format(event))

    calendarCmds.close()

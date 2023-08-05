# -*- coding: utf-8 -*-

###
# Author: Vincent Lucas <vincent.lucas@gmail.com>
###

#import pytz
from dateutil.parser import *
from dateutil.relativedelta import *
from dateutil.tz import *
import datetime
import vobject
from vobject.base import ParseError

from .log import logger
from .DateUtils import DateUtils
from .VEvent import VEvent

###
# Class to manage calendars.
###
class VCalendar:
    ###
    # Instantiates an new calendar with the provided vCalendar text if any
    # provided.
    #
    # @param vcalendar_test The calendar text with vCalendar format.
    ###
    def __init__(
            self,
            vcalendar_text = None):

        self.vcalendar = None
        self.parse(vcalendar_text)
        self.vevents = []

    ###
    # Parse and load the provided vCalendar text.
    #
    # @param vcalendar_test The calendar text with vCalendar format.
    ###
    def parse(
            self,
            vcalendar_text = None):

        if(vcalendar_text != None):
            try:
                self.vcalendar = vobject.readOne(vcalendar_text)
            except ParseError as parse_error:
                self.__init__(None)
                logger.error(
                    "failed to parse the event: {0}\n{1}".format(
                        parse_error,
                        vcalendar_text))

    ###
    # Read an .ics file.
    #
    # @param filename An .ics filename containing an or several events.
    ###
    def read(
            self,
            filename):
        # Reads the .ics file.
        with open(filename, 'r', encoding='utf8', errors="backslashreplace") \
                as fd:
            self.parse(fd.read())

    ###
    # Returns the event uids from this calendar.
    #
    # @return The event uid list. Returns an empty list if this calendar does
    # not contain any event.
    ###
    def get_uids(
            self):
        uids = []
        for vevent in self.get_vevents():
            uids.append(vevent.get_uid())

        return uids

    def get_event(
            self,
            uid):
        for vevent in self.get_vevents():
            if(vevent.get_uid() == uid):
                return vevent

        return None

    ###
    # Returns the vevent list.
    #
    # @return the vevent list.
    ###
    def get_vevents(
            self,
            start = None,
            end = None):
        # TODO: only removes entries which are not in interval
        self.events = []

        # No event is loaded, then return an empty list.
        if(self.vcalendar == None):
            return self.events

        if(start and end):
            tz = tzlocal()
            start_datetime = parse(start)
            start_datetime = start_datetime.astimezone(tz)
            end_datetime = parse(end)
            end_datetime = end_datetime.astimezone(tz)

#        print("CHENZO: vcalendar: {0}".format(self.vcalendar.prettyPrint()))

        for vevent in self.vcalendar.vevent_list:
            if(start and end):
                dtstart = vevent.getChildValue("dtstart")
                dtstart = DateUtils.to_datetime(dtstart)
                dtend = vevent.getChildValue("dtend")
                dtend = DateUtils.to_datetime(dtend)

                list_rrule = []
                rrule = vevent.getChildValue("rrule")
                if(rrule):
                    vevent.rruleset.count = 64
                    list_rrule = vevent.rruleset.between(
                            start_datetime,
                            end_datetime,
                            inc=True)


                if(dtstart and dtend):
                    if (len(list_rrule) > 0):

#                        print("CHENZO")
#                        self.pretty_print()

                        for rrule in list_rrule:
                            # Construct the event corresponding to the
                            # matching recurrence
                            rdelta = relativedelta(rrule, dtstart)
                            new_vevent = vobject.newFromBehavior('vevent')
                            new_vevent.copy(vevent)
                            rrule_vevent = VEvent(new_vevent)
                            rrule_vevent.modify_dates(rdelta)

                            self.vevents.append(rrule_vevent)
#                            print("OK rrule: " + str(rrule)
#                                    + "\nrdelta: " + str(rdelta)
#                                    + "\nvevent.dtstart: "
#                                    + str(vevent.getChildValue("dtstart", ""))
#                                    + ", vevent.summary: "
#                                    + vevent.getChildValue("summary", "")
#                                    + "\nrrule_vevent.dtstart: "
#                                    + str(rrule_vevent.get_start())
#                                    + ", rrule_vevent.summary: "
#                                    + rrule_vevent.get_summary()
#                                    )

                    if((dtstart >= start_datetime and dtstart <= end_datetime)
                        or (dtend >= start_datetime and dtend <= end_datetime)):
                        # Removes previous rrule occurence if a specific one is
                        # present
                        for old_vevent in self.vevents:
                            if(dtstart == old_vevent.get_start()
                                    and dtend == old_vevent.get_end()):
                                self.vevents.remove(old_vevent)

                        self.vevents.append(VEvent(vevent))
#                        print("real event OK dtstart: " + str(dtstart)
#                                + ", summary: "
#                                + vevent.getChildValue("summary", ""))

            else:
                self.vevents.append(VEvent(vevent))

        self.vevents = sorted(
                self.vevents,
                key=lambda vevent: vevent.get_start())

        return self.vevents

    ###
    # TODO
    ###
#    def create_vevent(
#            self,
#            summary,
#            dtstart = None,
#            dtend = None,
#            location = None,
#            attendees = None,
#            privacy_class = "PULBIC",
#            repeat = None):
#        self.vcalendar = vobject.iCalendar()
#        self.vcalendar.add('vevent')
#        self.vcalendar.vevent.add('summary').value = summary
#        self.vcalendar.vevent.add('dtstart').value = datetime.datetime()



    def create(
            self,
            summary,
            start_date,
            end_date,
            location = None,
            description = None,
            attendees = None,
            recurrence_frequency_nb_occurences_per_unit_time = None,
            recurrence_frequency_unit_time = None,
            recurrence_nb = None,
            recurrence_end_date = None):

        self.vcalendar = vobject.iCalendar()
        self.vcalendar.add('prodid').value = 'memorandum'

        self.vcalendar.add('vevent')
        vevent = VEvent(self.vcalendar.vevent)
        vevent.create(
                summary,
                start_date,
                end_date,
                location,
                description,
                attendees,
                recurrence_frequency_nb_occurences_per_unit_time,
                recurrence_frequency_unit_time,
                recurrence_nb,
                recurrence_end_date)

    def get_stream(
            self):
        return self.vcalendar.serialize()

    ###
    # Print this calendar in a pleasant way.
    ###
    def pretty_print(
            self):
        self.vcalendar.prettyPrint()

    ###
    # Print a brief description of this calendar events.
    ###
    def print(
            self):
        for vevent in self.vcalendar.vevent_list:
            VEvent.print(vevent)

    ###
    # Returns the text serialized form of this calendar.
    #
    # @return The text serialized form of this calendar.
    ###
    def __repr__(
            self):
        return self.__str__()

    ###
    # Returns the text serialized form of this calendar.
    #
    # @return The text serialized form of this calendar.
    ###
    def __str__(
            self):
        return self.vcalendar.serialize()

###
# Author: Vincent Lucas <vincent.lucas@gmail.com>
###

import vobject
import xml.etree.ElementTree as XmlElementTree

from .CalDavSession import CalDavSession
from .DateUtils import DateUtils
from .VCalendar import VCalendar
from .VEvent import VEvent

###
# Calendar commands class.
# This is the interface used by all HCI to request the calendar service.
###
class CalendarCmds:
    ###
    # Creates a new calendar connection based on the configuration provided.
    #
    # @param conf The account configuration to connect to the server. It is a
    # dictionnary containing an "user", a "password" and an "url".
    ###
    def __init__(
            self,
            conf):
        self.calDavSession = CalDavSession(
                conf["user"],
                conf["password"],
                conf["url"])

    ###
    # Closes the connection to the server.
    ###
    def close(
            self):
        self.calDavSession.close()

    ###
    # Get an event based on his uid.
    #
    # @param uid The event uid to look for.
    #
    # @return The corresponding VEvent or None if not found.
    ###
    def get_event(
            self,
            uid):
        vcalendar_stream = self.calDavSession.get_event(uid)
        if(vcalendar_stream):
            vcalendar = VCalendar(vcalendar_stream)
            return vcalendar.get_event(uid)
        return None

    ###
    # Get event list between start and end provided dates.
    #
    # @param start The start date.
    # @param end The end date.
    #
    # @return The correspondings VEvent list or None if not found.
    ###
    def get_events(
            self,
            start,
            end):
        vevents = []
        xml = self.calDavSession.get_events(start, end)
        xml_root = XmlElementTree.fromstring(xml)
        for calendar in xml_root.iter(
                '{urn:ietf:params:xml:ns:caldav}calendar-data'):
            vcalendar = VCalendar(calendar.text)
            vevents = vevents + vcalendar.get_vevents(start, end)

        # Sort vevents by start date
        return sorted(vevents, key=lambda vevent: vevent.get_start())


    ###
    # Retrieves the event for the given day.
    #
    # @param day The date to retrieve. Or today if equal to None.
    #
    # @return The correspondings VEvent list or None if not found.
    ###
    def get_events_day(
            self,
            day = None):

        # Compute start day
        if(day != None):
            start_day = DateUtils.get_datetime(day)
        else:
            start_day = DateUtils.get_day_start(0)

        # Compute next day
        next_day = DateUtils.get_day_end(0, start_day)

        # Converts to datetime
        start = DateUtils.get_caldav_string(start_day)
        end = DateUtils.get_caldav_string(next_day)

        return self.get_events(start, end)

    ###
    # Retrieves the event for the given week.
    #
    # @param day The date from a day in the requested week. Or this week if
    # equal to None.
    #
    # @return The correspondings VEvent list or None if not found.
    ###
    def get_events_week(
            self,
            day = None):

        # Compute daytime
        if(day != None):
            search_day = DateUtils.get_datetime(day)
        else:
            search_day = DateUtils.get_day_start(0)

        start_day = DateUtils.get_weekday_start(search_day)
        end_day = DateUtils.get_weekday_end(search_day)

        # Converts to datetime
        start = DateUtils.get_caldav_string(start_day)
        end = DateUtils.get_caldav_string(end_day)

        return self.get_events(start, end)

    ###
    # Retrieves the event for the given month.
    #
    # @param day The date from a day in the requested month. Or this month if
    # equal to None.
    #
    # @return The correspondings VEvent list or None if not found.
    ###
    def get_events_month(
            self,
            day = None):

        # Compute daytime
        if(day != None):
            search_day = DateUtils.get_datetime(day)
        else:
            search_day = DateUtils.get_day_start(0)

        start_day = DateUtils.get_monthday_start(search_day)
        end_day = DateUtils.get_monthday_end(search_day)

        # Converts to datetime
        start = DateUtils.get_caldav_string(start_day)
        end = DateUtils.get_caldav_string(end_day)

        return self.get_events(start, end)

    ###
    # Creates a new event with the provided parameters.
    #
    # @param summary The summary for the new event.
    # @param start_date The start date for the new event.
    # @param end_date The end date for the new event.
    # @param location The location for the new event.
    # @param description The description for the new event.
    # @param attendees TODO The attendees for the new event.
    # @param recurrence_frequency The recurrence frequency for the new event:
    #       DAILY, WEEKLY, MONTHLY, YEARLY
    # @param recurrence_interval The recurrence interval for the new event (use
    #       it with recurrence_frequency):
    # e.g. 1 for each day, 2 for each two days
    # @param recurrence_count The maximal number of recurrences for the new
    #       event.
    # @param recurrence_end_date The maximale end date for the recurrences of
    #       the new event.
    #
    # @return The uid from the created event
    ###
    def create_event(
            self,
            summary,
            start_date,
            end_date,
            location = None,
            description = None,
            attendees = None, # TODO
            recurrence_frequency = None,
            recurrence_interval = None,
            recurrence_count = None,
            recurrence_end_date = None):
        uid = None

        vcalendar = VCalendar()
        vcalendar.create(
                summary,
                start_date,
                end_date,
                location,
                description,
                attendees,
                recurrence_frequency,
                recurrence_interval,
                recurrence_count,
                recurrence_end_date)

        if(self.calDavSession.set_event(
                vcalendar.get_stream(),
                vcalendar.get_uids()[0])):
            uid = vcalendar.get_uids()[0]

        return uid

    ###
    # Delete the provided VEvent from the server.
    #
    # @param vevent The VEvent to delete
    ###
    def delete_event(
            self,
            vevent):
        return self.calDavSession.delete_event(vevent.get_uid())

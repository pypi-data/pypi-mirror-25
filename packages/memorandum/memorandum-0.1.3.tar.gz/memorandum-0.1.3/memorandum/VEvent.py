###
# Author: Vincent Lucas <vincent.lucas@gmail.com>
###

import random
import string
import vobject

from .DateUtils import DateUtils

###
# VEvent class.
###
class VEvent:
    def __init__(
            self,
            vevent):
        self.vevent = vevent;

    def set_value(
            self,
            key,
            value):
        if(self.vevent):
            if(self.vevent.getChildValue(key)):
                self.vevent.__setattr__(key, value)
            else:
                self.vevent.add(key).value = value

    def get_summary(
            self):
        return self.vevent.getChildValue("summary")

    def set_summary(
            self,
            summary):
        self.set_value("summary", summary)

    def get_location(
            self):
        return self.vevent.getChildValue("location")

    def set_location(
            self,
            location):
        self.set_value("location", location)

    def get_start(
            self):
        return DateUtils.to_datetime(
                self.vevent.getChildValue("dtstart"))

    def set_start(
            self,
            datetime):
        self.set_value("dtstart", datetime)

    def get_end(
            self):
        return DateUtils.to_datetime(
                self.vevent.getChildValue("dtend"))

    def set_end(
            self,
            datetime):
        self.set_value("dtend", datetime)

    def modify_dates(
            self,
            datetime_delta):
        if(self.vevent):
            if(self.vevent.dtstart and self.vevent.dtend):
                self.vevent.dtstart.value += datetime_delta
                self.vevent.dtend.value += datetime_delta

    def get_organizer(
            self):
        pass

    def set_organizer(
            self):
        pass

    def get_attendee_list(
            self):
        pass

    def add_attendee(
            self):
        pass

    def remove_attendee(
            self):
        pass

    def set_attendee_status(
            self):
        pass

    def download(
            self):
        # get event on serveur
        # then saves it to this object
        #self.vevent = vevent;
        pass

    def upload(
            self):
        pass

    def __str__(
            self):
        return str(self.vevent.prettyPrint())

    def get_short_str(
            self):
        location = self.vevent.getChildValue("location")
        summary = self.vevent.getChildValue("summary", "")
        dtstart = self.vevent.getChildValue("dtstart")
        dtend = self.vevent.getChildValue("dtend")

        event_str = ""

        # Location and summary
        if(location):
            event_str += "[" + location + "] - "
        event_str += summary

        # Start and end dates
        if(dtstart and dtend):
            start_day = dtstart.strftime("%d/%m/%Y")
            end_day = dtend.strftime("%d/%m/%Y")
            end_another_day = ""
            event_str += "\n[" + start_day + "] " + dtstart.strftime("%H:%M")
            if(start_day != end_day):
                end_another_day = "[" + end_day + "] "
            event_str += \
                " - " + end_another_day + dtend.strftime("%H:%M")


        return event_str

    def get_long_str(
            self):
        organizer = self.vevent.getChildValue("organizer")
        attendee_list = self.vevent.getChildValue("attendee")

        # Get short string : location, summary, start and end dates
        event_str = self.get_short_str()

        # Organizer
        event_str += "\n----\n"
        if(organizer):
            event_str += self.vevent.organizer.CN_param + " [ORGANIZER]\n"

        # Attendees
        if attendee_list:
            attendee_list_sorted = sorted(
                    self.vevent.attendee_list,
                    key = lambda attendee: attendee.CN_param)
            for attendee in attendee_list_sorted:
                event_str += attendee.CN_param \
                    + " [" + attendee.PARTSTAT_param + "]\n"

        return event_str

    ###
    # Set participation status (RFC 5545).
    #
    # @param vevent The event to modify.
    # @param email The user email for which the participation is set.
    # @param parstat The participation state :
    #   - NEEDS-ACTION
    #   - ACCEPTED
    #   - DECLINED
    #   - TENTATIVE
    #   - DELEGATED
    ###
    def set_partstat(
            vevent,
            email,
            partstat):
        email_str = "mailto:"+email
        for attendee in vevent.attendee_list:
            if(attendee.value == email_str):
                vevent.attendee.PARTSTAT_param = [ partstat ]

    ###
    # Return the uid of the given VEvent.
    #
    # @param event The provided VEvent.
    #
    # @return The Vevent uid value or an empty string if it does not exists.
    ###
    def get_uid(
            self):
        return self.vevent.getChildValue("uid", "")

    def set_uid(
            self,
            uid = None):
        if(uid == None):
            uid = self.get_random_uid()
        self.set_value("uid", uid)

    def set_recurrence(
            self,
            recurrence_frequency = None,
            recurrence_interval = None,
            recurrence_count = None,
            recurrence_end_date = None):
        if(recurrence_frequency
                and recurrence_interval
                and (recurrence_count or recurrence_end_date)):

            if(recurrence_count):
                recurrence = "FREQ={0};INTERVAL={1};COUNT={2}".format(
                        recurrence_frequency,
                        recurrence_interval,
                        recurrence_count)
            else: # recurrence_end_date_str
                recurrence_end_date_str = DateUtils.get_caldav_string(
                        recurrence_end_date)
                recurrence = "FREQ={0};INTERVAL={1};UNTIL={2}".format(
                        recurrence_frequency,
                        recurrence_interval,
                        recurrence_end_date_str)

            self.set_value("rrule", str(recurrence))

    ###
    # TODO
    ###
#    def create_vevent(
#            vevent,
#            summary,
#            dtstart = None,
#            dtend = None,
#            location = None,
#            attendees = None,
#            privacy_class = "PULBIC",
#            repeat = None):
#        vcalendar = vobject.iCalendar()
#        vcalendar.add('vevent')
#        vcalendar.vevent.add('summary').value = summary
#        vcalendar.vevent.add('dtstart').value = datetime.datetime()

    def create(
            self,
            summary,
            start_date,
            end_date,
            location = None,
            description = None,
            attendees = None,
            recurrence_frequency = None,
            recurrence_interval = None,
            recurrence_count = None,
            recurrence_end_date = None):

        # Commented to let vobject autogenerate it.
        self.set_uid()
        self.set_summary(summary)
        self.set_start(start_date)
        self.set_end(end_date)
        self.set_recurrence(
                recurrence_frequency,
                recurrence_interval,
                recurrence_count,
                recurrence_end_date)

    def get_random_uid(
            self,
            size=32):
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(size))

###
# Author: Vincent Lucas <vincent.lucas@gmail.com>
###

import requests

###
# Class that manage the CalDav connection with the server.
###
class CalDavSession:
    ###
    # Initialize the CalDav parameters but does not connect to the server.
    #
    # @param user The user login.
    # @param password The user password.
    # @param url The base url to connect to.
    ###
    def __init__(
            self,
            user,
            password,
            url):

        self.session = requests.Session()
        self.session.auth = (user, password)
        self.url = url

    ###
    # Close the CalDav connection.
    ###
    def close(
            self):
        self.session.close()

    ###
    # Get the requested event from the server.
    #
    # @param eventid The id of the event to return.
    #
    # @return The requested event text. Or an empty string if the event is not
    # found.
    ###
    def get_event(
        self,
        eventid):

        value = ""
        caldav_content_type = 'text/calendar; charset=utf8'

        result = self.session.get(self.url + "/" + eventid + ".ics")
        if(result.status_code == 200
                and result.headers['content-type'] == caldav_content_type):
            value = result.text

        return value

    ###
    # Creates or updates the event on the server.
    #
    # @param event The event text.
    # @param eventid The event id.
    #
    # @return True if the event is succefully created or modified. False,
    # otherwise.
    ###
    def set_event(
        self,
        event,
        eventid):

        result = self.session.put(self.url + "/" + eventid + ".ics", data=event)
        #result = self.session.put(self.url, data=event)

        # created == 201, modified == 204
        return (result.status_code == 201
                or result.status_code == 204)

    ###
    # Delete the requested event.
    #
    # @param eventid The veznt id.
    #
    # @return True if the event is succefully deleted. False, otherwise.
    ###
    def delete_event(
            self,
            eventid):

        result = self.session.delete(self.url + "/" + eventid + ".ics")

        # modified == 204
        return (result.status_code == 204)

    ###
    # List the calendar matching given date interval.
    #
    # @param start_date The interval start date.
    # @param end_date The interval end date.
    #
    # @return The list of corresponding events. An empty list if none was found.
    ###
    def list_calendar_collections(
            self):
#        Example:
#            <C:calendar-home-set xmlns:D="DAV:"
#                    xmlns:C="urn:ietf:params:xml:ns:caldav">
#                <D:href>http://cal.example.com/home/bernard/calendars/</D:href>
#            </C:calendar-home-set>
        pass

    ###
    # Get events from the server corresponding to the requested interval.
    #
    # @param start The start date of the time interval.
    # @param end The end date of the time interval.
    #
    # @return The events for this interval. Or an empty string if no event
    # correspond.
    ###
    def get_events(
            self,
            start,
            end):

        value = ""
        caldav_content_type = 'text/xml; charset="utf-8"'

        method = "REPORT"
        url = self.url
        headers = {
                "Content-Type": "application/xml; charset=\"utf-8\"",
                "Prefer": "return-minimal",
                "Depth": "1"
        }

        event_date_filter = ''
        if(start and end):
            event_date_filter = '''
			    <C:time-range
                                start="''' + start +  '''"
				  end="''' + end + '''" />
                '''

        data = '''
	    <?xml version="1.0" encoding="utf-8" ?>
	    <C:calendar-query
		    xmlns:D="DAV:"
		    xmlns:C="urn:ietf:params:xml:ns:caldav">
		<D:prop>
                    <D:getetag/>
		    <C:calendar-data />
		</D:prop>
		<C:filter>
		    <C:comp-filter name="VCALENDAR">
			<C:comp-filter name="VEVENT">
                            {0}
			</C:comp-filter>
		    </C:comp-filter>
		</C:filter>
	    </C:calendar-query>'''.format(event_date_filter)

        request = requests.Request(method, url, data=data, headers=headers)
        result = self.session.send(self.session.prepare_request(request))

        if(result.status_code == 207
                and result.headers['content-type'] == caldav_content_type):
            value = result.text

        return value

# N.B. create a new calendar via MKCALENDAR via DAV:displayname (exemple page
# 24)

# N.B. to create a vevent add the "If-None-Match: *" HTTP header to the PUT
# request.
# "If-Match: *" for updating.
#
# e.g.
#PUT /home/lisa/calendars/events/qwue23489.ics HTTP/1.1
#If-None-Match: *
#Host: cal.example.com
#Content-Type: text/calendar
#Content-Length: xxxx
#
#BEGIN:VCALENDAR
#VERSION:2.0
#PRODID:-//Example Corp.//CalDAV Client//EN
#BEGIN:VEVENT
#UID:20010712T182145Z-123401@example.com
#DTSTAMP:20060712T182145Z
#DTSTART:20060714T170000Z
#DTEND:20060715T040000Z
#SUMMARY:Bastille Day Party
#END:VEVENT
#END:VCALENDAR


# N.B. RRULE management : (see CALDAV:expand in Section 9.6.5.)

# N.B. event search
#REPORT /bernard/work/ HTTP/1.1
#Host: cal.example.com
#Depth: 1
#Content-Type: application/xml; charset="utf-8"
#Content-Length: xxxx
#<?xml version="1.0" encoding="utf-8" ?>
#<C:calendar-query xmlns:D="DAV:"
#xmlns:C="urn:ietf:params:xml:ns:caldav">
#
#<D:prop>
#    <D:getetag/>
#    <C:calendar-data>
#	<C:comp name="VCALENDAR">
#	    <C:prop name="VERSION"/>
#	    <C:comp name="VEVENT">
#	    <C:prop name="SUMMARY"/>
#	    <C:prop name="UID"/>
#	    <C:prop name="DTSTART"/>
#	    <C:prop name="DTEND"/>
#	    <C:prop name="DURATION"/>
#	    <C:prop name="RRULE"/>
#	    <C:prop name="RDATE"/>
#	    <C:prop name="EXRULE"/>
#	    <C:prop name="EXDATE"/>
#	    <C:prop name="RECURRENCE-ID"/>
#	</C:comp>
#	<C:comp name="VTIMEZONE"/>
#	</C:comp>
#    </C:calendar-data>
#</D:prop>
#<C:filter>
#    <C:comp-filter name="VCALENDAR">
#	<C:comp-filter name="VEVENT">
#	    <C:time-range start="20060104T000000Z" end="20060105T000000Z"/>
#	</C:comp-filter>
#    </C:comp-filter>
#</C:filter>
#</C:calendar-query>
#
#
#Partial Retrieval of Recurring Events: CALDAV:limit-recurrence-set
#Expanded Retrieval of Recurring Events: CALDAV:expand


# N.B. get event by id
#REPORT /bernard/work/ HTTP/1.1
#Host: cal.example.com
#Depth: 1
#Content-Type: application/xml; charset="utf-8"
#Content-Length: xxxx
#
#<?xml version="1.0" encoding="utf-8" ?>
#<C:calendar-query xmlns:C="urn:ietf:params:xml:ns:caldav">
#    <D:prop xmlns:D="DAV:">
#	<D:getetag/>
#	<C:calendar-data/>
#    </D:prop>
#    <C:filter>
#	<C:comp-filter name="VCALENDAR">
#	    <C:comp-filter name="VEVENT">
#		<C:prop-filter name="UID">
#		<C:text-match collation="i;octet">DC6C50A017428C5216A2F1CD@example.com</C:text-match>
#		</C:prop-filter>
#	    </C:comp-filter>
#	</C:comp-filter>
#    </C:filter>
#</C:calendar-query>

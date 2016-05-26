try:
    # Python 2 libraries.
    from urllib2 import urlopen
    from HTMLParser import HTMLParser
except ImportError:
    # Python 3 libraries.
    from urllib.request import urlopen
    from html.parser import HTMLParser


import time
import xml.etree.ElementTree as ET


class SteamXMLParser(HTMLParser):
    def __init__(self, id):
        # Old style class constructor
        HTMLParser.__init__(self)

        self.url = "http://steamcommunity.com/gid/$id/" \
                   "events?xml=1&action=eventFeed&month=$month&year=$year"

        '''
          id converted to string so it can be inserted into the url.
          Has to be the numeric id of the group, NOT the name.
        '''
        self.id = str(id)
        self.isParsing = False
        self.important_tags = ["span", "a"]

        # The XML tags for the events.
        self.event_tags = ["event", "expiredEvent"]
        self.data_types = ["Date", "Time", "Message"]
        self.data_count = len(self.data_types)

        # The data yielded by the parse_xml method
        self.curr_event = {"Date": "", "Time": "",
                           "Message": ""}
        self.counter = 0

    def get_event_list(self):
        """
            Returns a list of dictionaries all the current event
        """
        return list(self.iterate_events())

    def iterate_events(self):
        """
        Wrapper around the _parse_xml method
        Yields a dictionary with the date, time,
          message and comment count of each event.
        """
        for x in self._parse_xml(self._load_data()):
            yield x

    def handle_starttag(self, tag, attrs):
        """
        Overloaded method from the HTMLParser class.
        Passes the data to handle_data.
        The only tags looked at are 'a' and 'span'
        """
        if (tag in self.important_tags):
            self.isParsing = True
        else:
            self.isParsing = False

    def handle_data(self, data):
        """
        Overloaded method from the HTMLParser class.
        Set the current event value to the values passed from the HTML data.
        Only looks through the first three elements (Date, Time and Message)
        """

        # Remove \t and \n
        data = data.strip()
        if (self.isParsing and self.counter < self.data_count and data != ""):
            # Set the values of the current event dictionary.
            # This is then returned in the parse_event function.
            self.curr_event[self.data_types[self.counter]] = data
            self.counter += 1

    def _load_data(self):
        """Download the XML file"""
        return urlopen(self._format_url(self.url)).read()

    def _format_url(self, url):
        """ Inserts the appropriate month, year and id into the steam url"""
        return url.replace("$month", self._get_month()).replace(
                            "$year", self._get_year()).replace(
                                    "$id", self.id)

    def _parse_xml(self, xml):
        """
        A generator that
        returns all the individual
        events from a steam group
        """
        doc = ET.fromstring(xml)
        # Check if the response code is 'OK'
        if (doc.find("results").text == "OK"):
            for event in doc.iter():
                if event.tag in self.event_tags:
                    yield self.parse_event(event.text)

        else:
            raise Exception("Response not OK")

    def parse_event(self, text):
        """
        Passes the HTML string from the XML component
        into the HTMLParser.

        returns a curr_event dictionary
        with filled in Date, Time and Message.

        """
        self.feed(text)
        self.counter = 0
        return self.curr_event

    """Returns the current month as a number"""
    def _get_month(self):
        return time.strftime("%m")

    """Returns the current year as a number"""
    def _get_year(self):
        return time.strftime("%Y")

if __name__ == "__main__":
    import argparse
    arg_parser = argparse.ArgumentParser(description="\
            Return a list of events for a given group.")
    arg_parser.add_argument("id", type=str)

    args = arg_parser.parse_args()

    event_parser = SteamXMLParser(args.id)
    for event in event_parser.iterate_events():
        print(event)

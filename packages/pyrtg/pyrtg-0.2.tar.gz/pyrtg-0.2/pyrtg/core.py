# -*- coding: utf-8 -*-

class Sensor(object):
    """ PRTG sensor. At this time, simply contains channels.
    """
    id = 0
    name = ""
    channels = []

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def add_channel(self, channel):
        self.channels.append(channel)

    def generate_xml(self):
        xml = "<prtg>\n"
        for channel in self.channels:
            xml += channel.get_xml()
        xml += "</prtg>"
        return xml

    def generate_json(self):
        json_string = '{"prtg": {"result": ['
        for channel in self.channels:
            json_string += channel.get_json()
        json_string = json_string[:-1] # this removes the last comma after the last channel
        json_string += "]}}"
        return json_string

class Channel(object):
    """ PRTG channel. These get added to Sensor objects.
    """

    id = 0
    name = ""
    value = 0
    extra_fields = {}

    def __init__(self, id, name, value):
        self.id = id
        self.name = name
        self.value = value

    # <LimitMinWarning>0.5</LimitMinWarning><LimitWarningMsg>Peer is not active.</LimitWarningMsg><LimitMode>1</LimitMode></result>
    def set_extra_fields(self, field_name, field_value):
        self.extra_fields[field_name] = field_value

    def get_xml(self):
        xml = "<result>"
        xml += "<channel>%s</channel><value>%s</value>" % \
              (self.name, self.value)
        # extra fields is used to set additiona stuff, ie. "LimitMinWarning"
        # without having to add all of it here
        for entry in self.extra_fields:
                xml += "<%s>%s</%s>" % (entry,self.extra_fields[entry],entry)
        xml += "</result>\n"
        return xml

    def get_json(self):
        json_str = '{"channel": "%s", "value": "%s"},' % (self.name, self.value)
        return json_str
        
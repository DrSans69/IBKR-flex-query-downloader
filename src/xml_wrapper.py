import xml.etree.ElementTree as ET


def get_tag_value(xml_string, tag):
    try:
        root = ET.fromstring(xml_string)
        element = root.find('.//' + tag)
        if element is not None:
            return element.text
    except ET.ParseError:
        pass
    return None

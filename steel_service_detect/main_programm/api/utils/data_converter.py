import json
import xml.etree.ElementTree as ET

def json_to_xml(json_obj, line_padding=""):
    """Convert JSON object to XML string."""
    result_list = []

    json_obj_type = type(json_obj)

    if json_obj_type is list:
        for sub_elem in json_obj:
            result_list.append(json_to_xml(sub_elem, line_padding))
        return "\n".join(result_list)

    if json_obj_type is dict:
        for tag_name in json_obj:
            sub_obj = json_obj[tag_name]
            result_list.append("%s<%s>" % (line_padding, tag_name))
            result_list.append(json_to_xml(sub_obj, "\t" + line_padding))
            result_list.append("%s</%s>" % (line_padding, tag_name))
        return "\n".join(result_list)
    return "%s%s" % (line_padding, json_obj)

def xml_to_json(xml_str):
    """Convert XML string to JSON object."""
    root = ET.fromstring(xml_str)
    return {root.tag: _xml_to_json(root)}

def _xml_to_json(element):
    """Helper function for xml_to_json."""
    if len(element) == 0:
        return element.text
    return {child.tag: _xml_to_json(child) for child in element}
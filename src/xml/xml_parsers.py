from lxml import etree

from .xml_errors import EmptyEntryError, NilEntryError


def _parse_tree(parent, parent_dict: dict) -> dict:
    if len(list(parent)) == 0:
        tag = parent.tag.split('}', maxsplit=1)[1]
        text = parent.text

        if text is None:
            raise EmptyEntryError(tag)

        if text.upper() == 'NIL':
            raise NilEntryError(tag)

        parent_dict.update({tag: text})
        return {}
    else:
        children_dict = {}
        for child in parent:
            _parse_tree(child, children_dict)

        tag = parent.tag.split('}', maxsplit=1)[1]
        if tag in parent_dict.keys():
            if isinstance(parent_dict[tag], dict):
                dict_list = [parent_dict[tag]]
                parent_dict.update({tag: dict_list})

            parent_dict[tag].append(children_dict)
        else:
            parent_dict.update({tag: children_dict})


def _parse_xml(path: str, remove_comments=True) -> dict:
    tree = etree.parse(path, parser=etree.XMLParser(remove_comments=remove_comments))
    root = tree.getroot()

    xml_dict = {}
    _parse_tree(root, xml_dict)

    return xml_dict

import xmltodict


def xmlparser(filepath):
    with open(filepath) as f:
        return xmltodict.parse(f.read())
import urllib2
import logging
import os
import copy
from lxml import etree
from lxml.etree import ElementTree
from collections import Counter


# Settings for the logger
logger = logging.getLogger(__name__)


class CMDOWS(object):
    """Class for with various methods for checking and manipulating CMDOWS files"""

    def __init__(self, file_path=None, element=None):
        if file_path:
            self.file = file_path
        if element is not None:
            self.root = ElementTree(element).getroot()
        if file_path and element is None:
            parser = etree.XMLParser(remove_blank_text=True)
            self.root = ElementTree(file=file_path, parser=parser).getroot()

    def version(self):
        """Method to retrieve the version of the CMDOWS file"""
        url_prefix = '{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation'
        version = self.root.attrib[url_prefix].split('/')[-2]
        version = str(version)
        return version

    def schema(self):
        """Method to retrieve a schema either belonging to the CMDOWS file"""
        version = self.version()
        try:
            url = 'https://bitbucket.org/imcovangent/cmdows/raw/master/schema/' + version + '/cmdows.xsd'
            schema_string = urllib2.urlopen(url).read()
        except (urllib2.URLError, OSError):
            logger.info('Could not reach the CMDOWS schema file online. A local copy is used.')
            versions = os.listdir(os.path.join(os.path.dirname(__file__), 'schemas'))
            if version in versions:
                schema_string = open(os.path.join(os.path.dirname(__file__), 'schemas/' + version + '/cmdows.xsd'),
                                     'r').read()
            else:
                raise IOError('The specified CMDOWS schema version could not be found. '
                              'Are you sure that version ' + version + ' is an official CMDOWS schema version?')
        schema = etree.XMLSchema(etree.XML(schema_string))
        return schema

    def simplify(self):
        """Method to simplify everything"""
        for name in dir(self):
            if name.startswith('simplify_'):
                method = getattr(self, name)
                method()

    def simplify_equations(self):
        """Method to replace duplicate equations elements by a single equations element and refs to this element"""
        # Make deepcopy of all equations (as some attributes are going to be deleted for the check)
        equations_xml = copy.deepcopy(self.root.xpath('.//equations'))
        # Create dictionary with all equations
        equations_dict = {}
        for equation in equations_xml:
            id = equation.attrib['uID']
            del equation.attrib['uID']
            equations_dict[id] = etree.tostring(equation)
        # Create reverse dictionary with all equations
        equations_dict_rev = {}
        for key, value in equations_dict.items():
            equations_dict_rev.setdefault(value, set()).add(key)
        # Find duplicates
        equations_duplicates = [values for key, values in equations_dict_rev.items() if len(values) > 1]
        # For every duplicate keep only the first equations element and replace other equations elements by a ref
        for equations_duplicate in equations_duplicates:
            for id in list(equations_duplicate)[1:]:
                old_equations_element = self.root.xpath('.//equations[@uID="' + id + '"]')[0]
                new_equations_element = etree.Element('equationsUID')
                new_equations_element.text = list(equations_duplicate)[0]
                old_equations_element.getparent().replace(old_equations_element, new_equations_element)

    def check(self):
        """Method to execute all checks"""
        result = True
        for name in dir(self):
            if name.startswith('check_'):
                method = getattr(self, name)
                result = result and method()
        return result

    def check_schema(self):
        """Method to check if a CMDOWS file adheres to its schema"""
        try:
            result = self.schema().validate(self.root)
        except:
            result = False
        if not result:
            logger.warning('The CMDOWS file does not adhere to its schema.')
        return result

    def check_uids(self):
        """Method so check if all uIDs are actually unique in a CMDOWS file"""
        ids = [element.attrib['uID'] for element in self.root.xpath('.//*[@uID]')]
        result = (len(ids) == len(set(ids)))
        if not result:
            duplicates = [k for k, v in Counter(ids).items() if v > 1]
            logger.warning('The following uIDs are not unique: ' + ', '.join(duplicates))
        return result

    def check_references(self):
        """Method to check if references are actually pointing to a uID in a CMDOWS file"""
        ids = [element.attrib['uID'] for element in self.root.xpath('.//*[@uID]')]
        references = [element.text for element in self.root.xpath('.//*[contains(name(), "UID")]')]
        invalids = list(set([reference for reference in references if reference not in ids]))
        result = (len(invalids) == 0)
        if not result:
            logger.warning('The following uIDs do not exist although they are referred to: ' + ', '.join(invalids))
        return result

    def resolve_uids(self):
        """Method to rename duplicate UIDs in a CMDOWS file"""
        logger.warning('The resolve_uids method is a hack and should not be used.')
        ids = [element.attrib['uID'] for element in self.root.xpath('.//*[@uID]')]
        result = (len(ids) == len(set(ids)))
        if not result:
            duplicates = [k for k, v in Counter(ids).items() if v > 1]
            for duplicate in duplicates:
                duplicate_elements = self.root.xpath('.//*[@uID="' + duplicate + '"]')
                for duplicate_id, duplicate_element in enumerate(duplicate_elements):
                    duplicate_element.attrib['uID'] = duplicate_element.attrib['uID'] + '_' + str(duplicate_id)

    def save(self, file_path=None, pretty_print=False, method='xml', xml_declaration=True, encoding='UTF-8'):
        """Method to save a manipulated CMDOWS file"""
        if file_path:
            file_path = file_path
        elif self.file:
            file_path = self.file
        else:
            raise IOError('Please specify the path for the CMDOWS file.')
        ElementTree(self.root).write(file_path, pretty_print=pretty_print, method=method,
                                     xml_declaration=xml_declaration, encoding=encoding)

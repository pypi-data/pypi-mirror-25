#!/usr/bin/env python3
'''Processor for GPX and LOG files
Author: Konrad Dryja
License: GPLv3'''

import argparse
import sys
import re
import time
import os
from copy import deepcopy
from datetime import datetime
from dateutil.parser import parse
from lxml import etree, objectify
from lxml.etree import XMLSyntaxError


def validate_gpx(xml_file):
    '''Function to validate GPX file against XSD schema of gpx file'''

    # Copy all GPX file's contents into a string variable.
    xml_string = xml_file.read()
    xml_file.close()

    # Obtain location of the XSD path (relatively to the current file location)
    xsd_file_location = os.path.join(os.path.dirname(__file__), 'gpx.xsd')

    # Try to parse the schema.
    try:
        # Declare schema to use.
        schema = etree.XMLSchema(file=xsd_file_location)

        # Create a parser which we will match against our xml string.
        parser = objectify.makeparser(schema=schema)

        # Match XSD with the XML file. Nothing will happen if successful.
        # XMLSyntaxError will be raised if unsuccessful.
        objectify.fromstring(str.encode(xml_string), parser)

    # Capture the exception.
    except XMLSyntaxError:
        # Print error message and exit the program.
        print('ERROR. Failed to validate the GPX file.')
        sys.exit(1)


def produce_output(gpx_file, log_file, verbose, merge, threshold, skip_value):
    '''Produce XML output containing information about waypoint (and possibly trackpoints)'''

    # Define our ranges on which we will base all colouring.
    base_range = range(-150, 15)
    green_range = range(threshold, 14)
    orange_range = range(-149, threshold + 1)
    red_range = range(-150, -149)

    # Reopen passed GPX file so we can read its contents.
    gpx_file = open(gpx_file.name, 'r')

    # Parse the gpx file into lxml structure
    # Strip all blank space from the XML file using etree parser
    parser = etree.XMLParser(remove_blank_text=True)
    parsed_gpx = etree.parse(gpx_file, parser).getroot()

    # Every field has appended namespace.
    # So to search for them efficiently, we will need to extract it from the original xml.
    # Later we will append it in front of every field.
    xml_namespace = '{' + parsed_gpx.nsmap[None] + '}'

    # Create our output XML tree and append the root element - gpx
    outputxml_root = etree.Element('gpx')

    # Set metadata of our xml output file.
    outputxml_root.set('version', '1.1')

    # Set namespace of our xml output file.
    outputxml_root.set('xmlns', parsed_gpx.nsmap[None])
    # Initiate our dictionary containing all trackpoints.
    trackpoints_dict = {}

    # For every element in our parsed gpx called trkpt (i.e. all track points and their data)
    for element in parsed_gpx.findall('.//' + xml_namespace + 'trkpt'):

        # Extract and parse the timestamp stored under 'time' element as text
        # Also remove the time offset info, since it's 0 anyway and breaks comparison later on.
        waypoint_timestamp = parse(element.find(
            xml_namespace + 'time').text).replace(tzinfo=None)

        # Every timestamp will be a key in our dictionary.
        # Every key will contain a list where first element is latitude
        # Second element is longitude
        # And third element is 'ele' from the gpx file
        trackpoints_dict[waypoint_timestamp] = []
        trackpoints_dict[waypoint_timestamp].append(element.attrib['lat'])
        trackpoints_dict[waypoint_timestamp].append(element.attrib['lon'])
        trackpoints_dict[waypoint_timestamp].append(
            element.find(xml_namespace + 'ele').text)

    # Initiate iterator according to the "skip" variable
    skip_iterator = 0

    for line in log_file:

        # Only check lines containing PeerRSSI (we don't care about others).
        if 'PeerRSSI' in line:

            # If it is not ours skip_value'th iteration, skip the line
            # Also increase the iterator
            if (skip_iterator % skip_value) != 0:
                skip_iterator += 1
                continue
            skip_iterator += 1

            # Extract Date from the log and PeerRSSI value
            # Using regular expression.
            regex_match = re.match(r'(.*\;.*);.*PeerRSSI:(-\d+)', line)

            # Need to strip time to match our format.
            # It is matched as the first group from regex.
            log_struct_time = time.strptime(
                regex_match.group(1), '%Y.%m.%d;%H:%M:%S.%f')

            # Convert time.struct_time to datetime so we can compare them.
            log_datetime = datetime.fromtimestamp(time.mktime(log_struct_time))

            # If PeerRSSI is outside -148 and +14 range, omit the entry and report to stderr
            if int(regex_match.group(2)) not in base_range:
                sys.stderr.write(
                    'TIMESTAMP FROM .LOG: {}\n'.format(log_datetime))
                sys.stderr.write(
                    'PeerRSSI FROM .LOG: {}\n'.format(regex_match.group(2)))
                sys.stderr.write(
                    'PeerRSSI OUTSIDE -148 AND +14 RANGE. SKIPPING.\n\n')
                continue

            # Find the closest timestamp from the GPX file.
            # This will be the minimal absolute of subtraction across every date.
            closest_date = min(trackpoints_dict.keys(),
                               key=lambda x: abs(x - log_datetime))

            # Add new waypoint to our output XML file.
            waypoint = etree.SubElement(outputxml_root, 'wpt')

            # Add both lat and lon as an attribute of the wpt
            waypoint.attrib['lat'] = trackpoints_dict[closest_date][0]
            waypoint.attrib['lon'] = trackpoints_dict[closest_date][1]

            # Add symbol element to the waypoint.
            symbol = etree.SubElement(waypoint, 'sym')

            # Depending on the value of the PeerRSSID, set corresponding waypoint colour.
            if int(regex_match.group(2)) in green_range:
                symbol.text = 'Navaid, Green'
            if int(regex_match.group(2)) in orange_range:
                symbol.text = 'orange-blank'
            if int(regex_match.group(2)) in red_range:
                symbol.text = 'Navaid, Red'

            # If verbose flag has been set, output debug info to the stderr.
            if verbose:
                sys.stderr.write(
                    'TIMESTAMP FROM .LOG: {}\n'.format(log_datetime))
                sys.stderr.write(
                    'PeerRSSI FROM .LOG: {}\n'.format(regex_match.group(2)))
                sys.stderr.write(
                    'MATCHED LAT FROM .GPX: {}\n'.format(waypoint.attrib['lat']))
                sys.stderr.write(
                    'MATCHED LON FROM .GPX: {}\n\n'.format(waypoint.attrib['lon']))

    # At the very end, if "--merge" flag has been set, append all tracks to the file.
    if merge:
        # To achieve this, we locate the <trk> tag (that's first one) in our original gpx
        # and append it to our output xml.
        outputxml_root.append(deepcopy(parsed_gpx[1]))

        # Also change the colour of the track to 0000ff.
        outputxml_root.find(".//" + xml_namespace +
                            "extensions")[0].text = "0000ff"

    # Print our resulting XML file to the stdout.
    # Remembering about the xml declaration and to print it in a pretty format.

    print(etree.tostring(outputxml_root, pretty_print=True,
                         xml_declaration=True, encoding='UTF-8')
          .decode('UTF-8'))


def main():
    '''Main point of entry to the program'''

    # Define parser for command line arguments
    parser = argparse.ArgumentParser(description='Process GPX and LOG files.')

    # Add argument to fetch gpx file location and make sure it opens
    # (i.e. file exists and permissions are in order)
    parser.add_argument('gpx', metavar='*.gpx', type=argparse.FileType('r'),
                        help='.gpx file path')

    # Same as above but with log file.
    parser.add_argument('log', metavar='*.log', type=argparse.FileType('r'),
                        help='.log file path')

    # Capture whether user intends to run the program with increased verbosity level. Default false.
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='''report .log radio test numbers with associated .gpx lat/lon co-ords
                                to stderr during processing''')

    # Capture whether user intends to merge gpx and log files during execution. Defaults false.
    parser.add_argument('--merge', '-m', action='store_true',
                        help='''add radio tests as waypoints into the output file which combines the
                                trackpoints from .gpx and the radio tests from .log as waypoints''')

    # Allows user to enter his own threshold. If left blank, will use -125.
    parser.add_argument('--gothresh', type=int, action='store', metavar='[-148-14]',
                        choices=range(-148, 15),
                        help='''threshold in dBm between strong signal (green)
                                and marginal signal (orange). Default is -125.''',
                        default=49)

    # Allows user to enter his own skip every X value. If left blank, will use 1.
    parser.add_argument('--skip', type=int, action='store', metavar='[1-10]',
                        choices=range(1, 11),
                        help='''process only every Xth radio test. Default is 1.''',
                        default=1)

    # Parse all arguments to the Namespace object.
    args = parser.parse_args()

    # Save passed .gpx file to a variable.
    gpx_file = vars(args)['gpx']

    # Save passed .log file to a variable.
    log_file = vars(args)['log']

    # Save whether to run the program in increase verbosity
    verbose = vars(args)['verbose']

    # Save whether to merge .gpx with .log
    merge = vars(args)['merge']

    # Save passed threshold value.
    threshold = vars(args)['gothresh']

    # Save passed skip value.
    skip_value = vars(args)['skip']

    # Validate passed .gpx file against .xsd schema.
    validate_gpx(gpx_file)

    # Go through the files and produce the output.
    produce_output(gpx_file, log_file, verbose, merge, threshold, skip_value)


# Start function main() if it is the main entry point.
if __name__ == '__main__':
    main()

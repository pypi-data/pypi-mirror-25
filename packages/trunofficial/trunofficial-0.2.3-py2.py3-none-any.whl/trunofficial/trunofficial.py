#!/usr/bin/env python

try:
    from urllib import urlopen
    from urllib import urlencode
except ImportError:
    from urllib.request import urlopen
    from urllib.parse import urlencode

import json
import six
import argparse


class TruecallerError(Exception):
    def __init__(self, message=None):
        super(TruecallerError, self).__init__(message)


def search(*numbers, **kwargs):
    if 'cc' in kwargs:
        cc = kwargs['cc']
    else:
        cc = home_country()

    if len(numbers) > 1:
        results = []
        for number in numbers:
            response = lookup(number, cc)
            result = _Attributes(response)
            results.append(result)
    else:
        number = numbers[0]
        response = lookup(number, cc)
        results = _Attributes(response)

    return results


def lookup(number, cc):
    URL = 'https://search5.truecaller.com/v2/search?'

    raw_params = {
        'q': number,
        'countryCode': cc,
        'type': '4',
        'locAddr': '',
        'placement': 'SEARCHRESULTS,HISTORY,DETAILS',
        'clientId': '1',
        'myNumber': 'lS5757de85c2804a87d452c139OpYeO6gR6qlj0QFJJQMpo1',
        'registerId': '568140610',
        'encoding': 'json',
    }

    print(raw_params)

    params = urlencode(raw_params)
    url_params = URL + params
    response = urlopen(url_params).read()
    response = response.decode('utf-8')
    parsed = json.loads(response)

    try:
        response_code = parsed['code']
        response_message = parsed['message']
        six.raise_from(TruecallerError("Recieved error response: (" + str(response_code) + ") " + response_message + "."), None)
    except KeyError:
        pass

    return parsed


def get_arguments():
    parser = argparse.ArgumentParser(
        description='Unofficial API to the Truecaller phone number search.')

    parser.add_argument(
        'numbers',
        metavar='NUMBER',
        type=str,
        nargs='*',
        help='phone numbers to lookup on Truecaller')

    parser.add_argument(
        '-c',
        '--countrycode',
        type=str,
        default=None,
        help='prioritize search by country')

    return parser


def home_country():
    ipinfo = 'https://ipinfo.io/country'
    cc = urlopen(ipinfo).read()
    cc = cc.decode('utf-8')
    cc = cc.rstrip('\n')
    return cc


def command_line():
    parser = get_arguments()
    args = parser.parse_args()
    numbers = args.numbers

    if not args.numbers:
        parser.print_help()
        exit()

    cc = args.countrycode

    for number in numbers:
        try:
            owner = search(number, cc=cc)
            mobile = owner.phone
            house = owner.address
            print('')
            print('Owner Name    : ' + str(owner.name))
            print('Mobile Number : ' + str(mobile.number))
            print('Country Code  : ' + str(mobile.countrycode))
            print('City          : ' + str(house.city))
            print('Area          : ' + str(house.area))
            print('Mobile Carrier: ' + str(mobile.carrier))
            print('TimeZone      : ' + str(house.timezone))
            print('Score         : ' + str(owner.score))
            print('Spam Score    : ' + str(mobile.spamscore))
            print('Spam Type     : ' + str(mobile.spamtype))
            print('Phone Type    : ' + str(mobile.phonetype))
            print('Owner ID      : ' + str(owner.id))
            print('Access        : ' + str(owner.access))
            print('Enhanced      : ' + str(owner.enhanced))
            print('Internet Addr.: ' + str(owner.internet_address))
            print('Badges        : ' + str(owner.badges))
            print('Tags          : ' + str(owner.tags))
            print('Owner Sources : ' + str(owner.sources))
            print('')
        except TruecallerError:
            print('Phone number not found: ' + str(number))


class _Attributes:
    def __init__(self, parsed):

        try:
            basic = parsed['data'][0]
            phone_parsed = parsed['data'][0]['phones'][0]
            address_parsed = parsed['data'][0]['addresses'][0]

            self.phone = _Phone(phone_parsed)
            self.address = _Address(address_parsed)

            self.id = basic['id']
            self.name = basic['name']
            self.score = basic['score']
            self.access = basic['access']
            self.enhanced = basic['enhanced']
            self.internet_address = basic['internetAddresses']
            self.badges = basic['badges']
            self.tags = basic['tags']
            self.sources = basic['sources']

            self.provider = parsed['provider']
            self.trace = parsed['trace']
            self.sourcestats = parsed['stats']['sourceStats']

        except:
            six.raise_from(TruecallerError("Cannot find the number in Truecaller database, " + str(self.phone.number) + '.'), None)


class _Phone:
    def __init__(self, phone):
        self.national = phone['nationalFormat']
        self.dialcode = phone['dialingCode']
        self.countrycode = phone['countryCode']
        self.carrier = phone['carrier']
        try:
            self.numbertype = phone['numberType']
        except KeyError:
            self.numbertype = None
        try:
            self.number = phone['e164Format']
        except KeyError:
            self.number = None
        try:
            self.spamscore = phone['spamScore']
            self.spamtype = phone['spamType']
        except KeyError:
            self.spamscore = None
            self.spamtype = None
        self.phonetype = phone['type']


class _Address:
    def __init__(self, address):
        try:
            self.area = address['area']
            self.city = address['city']
            self.timezone = address['timeZone']
        except KeyError:
            self.area = None
            self.city = None
            self.timezone = None
        self.countrycode = address['countryCode']
        self.type = address['type']

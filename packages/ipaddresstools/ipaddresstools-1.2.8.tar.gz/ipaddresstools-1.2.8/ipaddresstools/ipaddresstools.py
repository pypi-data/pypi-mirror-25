#!/usr/bin/env python3
##########################################################
# Script Name: modIpAddressTools.py                      #
# Script Type: Python                                    #
# Updated By: Benjamin P. Trachtenberg                   #
# Date Written 1/11/2015                                 #
#                                                        #
# Description:                                           #
# Collection of tools for IP Address's                   #
#                                                        #
##########################################################
import logging
import re as __re
import ipaddress as __ipaddress
import random as __random
__author__ = 'Benjamin P. Trachtenberg'
__copyright__ = "Copyright (c) 2016, Benjamin P. Trachtenberg"
__credits__ = None
__license__ = 'The MIT License (MIT)'
__status__ = 'prod'
__version_info__ = (1, 2, 8)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'

LOGGER = logging.getLogger(__name__)

""" 
Dictionaries included in v1.0.0

__mask_conversion = Used to convert IP masks and such

"""

__mask_conversion = {
    0: {"OCT1": 0, "OCT2": 0, "OCT3": 0, "OCT4": 0, "MASK": "0.0.0.0", "INVMASK": "255.255.255.255",
        "CIDR": "0"},
    1: {"OCT1": 128, "OCT2": 0, "OCT3": 0, "OCT4": 0, "MASK": "128.0.0.0", "INVMASK": "127.255.255.255",
        "CIDR": "1"},
    2: {"OCT1": 192, "OCT2": 0, "OCT3": 0, "OCT4": 0, "MASK": "192.0.0.0", "INVMASK": "63.255.255.255",
        "CIDR": "2"},
    3: {"OCT1": 224, "OCT2": 0, "OCT3": 0, "OCT4": 0, "MASK": "224.0.0.0", "INVMASK": "31.255.255.255",
        "CIDR": "3"},
    4: {"OCT1": 240, "OCT2": 0, "OCT3": 0, "OCT4": 0, "MASK": "240.0.0.0", "INVMASK": "15.255.255.255",
        "CIDR": "4"},
    5: {"OCT1": 248, "OCT2": 0, "OCT3": 0, "OCT4": 0, "MASK": "248.0.0.0", "INVMASK": "7.255.255.255",
        "CIDR": "5"},
    6: {"OCT1": 252, "OCT2": 0, "OCT3": 0, "OCT4": 0, "MASK": "252.0.0.0", "INVMASK": "3.255.255.255",
        "CIDR": "6"},
    7: {"OCT1": 254, "OCT2": 0, "OCT3": 0, "OCT4": 0, "MASK": "254.0.0.0", "INVMASK": "1.255.255.255",
        "CIDR": "7"},
    8: {"OCT1": 255, "OCT2": 0, "OCT3": 0, "OCT4": 0, "MASK": "255.0.0.0", "INVMASK": "0.255.255.255",
        "CIDR": "8"},
    9: {"OCT1": 255, "OCT2": 128, "OCT3": 0, "OCT4": 0, "MASK": "255.128.0.0", "INVMASK": "0.127.255.255",
        "CIDR": "9"},
    10: {"OCT1": 255, "OCT2": 192, "OCT3": 0, "OCT4": 0, "MASK": "255.192.0.0", "INVMASK": "0.63.255.255",
         "CIDR": "10"},
    11: {"OCT1": 255, "OCT2": 224, "OCT3": 0, "OCT4": 0, "MASK": "255.224.0.0", "INVMASK": "0.31.255.255",
         "CIDR": "11"},
    12: {"OCT1": 255, "OCT2": 240, "OCT3": 0, "OCT4": 0, "MASK": "255.240.0.0", "INVMASK": "0.15.255.255",
         "CIDR": "12"},
    13: {"OCT1": 255, "OCT2": 248, "OCT3": 0, "OCT4": 0, "MASK": "255.248.0.0", "INVMASK": "0.7.255.255",
         "CIDR": "13"},
    14: {"OCT1": 255, "OCT2": 252, "OCT3": 0, "OCT4": 0, "MASK": "255.252.0.0", "INVMASK": "0.3.255.255",
         "CIDR": "14"},
    15: {"OCT1": 255, "OCT2": 254, "OCT3": 0, "OCT4": 0, "MASK": "255.254.0.0", "INVMASK": "0.1.255.255",
         "CIDR": "15"},
    16: {"OCT1": 255, "OCT2": 255, "OCT3": 0, "OCT4": 0, "MASK": "255.255.0.0", "INVMASK": "0.0.255.255",
         "CIDR": "16"},
    17: {"OCT1": 255, "OCT2": 255, "OCT3": 128, "OCT4": 0, "MASK": "255.255.128.0", "INVMASK": "0.0.127.255",
         "CIDR": "17"},
    18: {"OCT1": 255, "OCT2": 255, "OCT3": 192, "OCT4": 0, "MASK": "255.255.192.0", "INVMASK": "0.0.63.255",
         "CIDR": "18"},
    19: {"OCT1": 255, "OCT2": 255, "OCT3": 224, "OCT4": 0, "MASK": "255.255.224.0", "INVMASK": "0.0.31.255",
         "CIDR": "19"},
    20: {"OCT1": 255, "OCT2": 255, "OCT3": 240, "OCT4": 0, "MASK": "255.255.240.0", "INVMASK": "0.0.15.255",
         "CIDR": "20"},
    21: {"OCT1": 255, "OCT2": 255, "OCT3": 248, "OCT4": 0, "MASK": "255.255.248.0", "INVMASK": "0.0.7.255",
         "CIDR": "21"},
    22: {"OCT1": 255, "OCT2": 255, "OCT3": 252, "OCT4": 0, "MASK": "255.255.252.0", "INVMASK": "0.0.3.255",
         "CIDR": "22"},
    23: {"OCT1": 255, "OCT2": 255, "OCT3": 254, "OCT4": 0., "MASK": "255.255.254.0", "INVMASK": "0.0.1.255",
         "CIDR": "23"},
    24: {"OCT1": 255, "OCT2": 255, "OCT3": 255, "OCT4": 0, "MASK": "255.255.255.0", "INVMASK": "0.0.0.255",
         "CIDR": "24"},
    25: {"OCT1": 255, "OCT2": 255, "OCT3": 255, "OCT4": 128, "MASK": "255.255.255.128", "INVMASK": "0.0.0.127",
         "CIDR": "25"},
    26: {"OCT1": 255, "OCT2": 255, "OCT3": 255, "OCT4": 192, "MASK": "255.255.255.192", "INVMASK": "0.0.0.63",
         "CIDR": "26"},
    27: {"OCT1": 255, "OCT2": 255, "OCT3": 255, "OCT4": 224, "MASK": "255.255.255.224", "INVMASK": "0.0.0.31",
         "CIDR": "27"},
    28: {"OCT1": 255, "OCT2": 255, "OCT3": 255, "OCT4": 240, "MASK": "255.255.255.240", "INVMASK": "0.0.0.15",
         "CIDR": "28"},
    29: {"OCT1": 255, "OCT2": 255, "OCT3": 255, "OCT4": 248, "MASK": "255.255.255.248", "INVMASK": "0.0.0.7",
         "CIDR": "29"},
    30: {"OCT1": 255, "OCT2": 255, "OCT3": 255, "OCT4": 252, "MASK": "255.255.255.252", "INVMASK": "0.0.0.3",
         "CIDR": "30"},
    31: {"OCT1": 255, "OCT2": 255, "OCT3": 255, "OCT4": 254, "MASK": "255.255.255.254", "INVMASK": "0.0.0.1",
         "CIDR": "31"},
    32: {"OCT1": 255, "OCT2": 255, "OCT3": 255, "OCT4": 255, "MASK": "255.255.255.255", "INVMASK": "0.0.0.0",
         "CIDR": "32"}}

mask_conversion = __mask_conversion

""" 
Functions included in v1.0.0
ucast_ip_mask(ip_addr_and_mask, return_tuple=True)
ucast_ip(ip_addr, return_tuple=True)
mcast_ip_mask(ip_addr_and_mask, return_tuple=True)
mcast_ip(ip_addr, return_tuple=True)
cidr_check(cidr, return_cidr=True)
get_neighbor_ip(ip_addr, cidr="30")
whole_subnet_maker (ip_addr, cidr)

Functions included in v1.1.0
number_check(check, return_number=True)

Functions included in v1.1.1
subnet_range(ip_net, cidr)
all_subnets_possible(ip_net, cidr)

Functions included in v1.1.2
all_subnets_longer_prefix(ip_net, cidr)
all_subnets_shorter_prefix(ip_net, cidr, include_default=False)
all_subnets_possible(ip_net, cidr) = AllSubnetsPossibleLongerPrefix(strIpNet,strCidr)

Functions included in v1.2.1
ip_mask(ip_addr_and_mask, return_tuple=True):
ip(ip_addr, return_tuple=True):

Added to v1.2.3
mask_conversion = __mask_conversion

Added to v1.2.4
all_ip_address_in_subnet(ip_net, cidr)

Added to v1.2.5
random_cidr_mask(lowest_mask=16)
random_ucast_ip()
random_mcast_ip()
random_ucast_ip_mask(lowest_mask=16)
random_mcast_ip_mask(lowest_mask=16)

"""


def ucast_ip_mask(ip_addr_and_mask, return_tuple=True):
    """
    Function to check if a address is unicast and that the CIDR mask is good
    Args:
        ip_addr_and_mask: Unicast IP address and mask in the following format 192.168.1.1/24
        return_tuple: Set to True it returns a IP and mask in a tuple, set to False returns True or False

    Returns: see return_tuple for return options

    """
    regex_ucast_ip_and_mask = __re.compile("^((22[0-3])|(2[0-1][0-9])|(1[0-9][0-9])|([1-9]?[0-9]))\.((25[0-5])|(2[0-4][0-9])|(1[0-9][0-9])|([1-9]?[0-9]))\.((25[0-5])|(2[0-4][0-9])|(1[0-9][0-9])|([1-9]?[0-9]))\.((25[0-5])|(2[0-4][0-9])|(1[0-9][0-9])|([1-9]?[0-9]))/((3[0-2])|([1-2]?[0-9]))$")
    if return_tuple:
        while not regex_ucast_ip_and_mask.match(ip_addr_and_mask):
            print("Not a good unicast IP and CIDR mask combo.")
            print("Please try again.")
            ip_addr_and_mask = input("Please enter a unicast IP address and mask in the follwing format x.x.x.x/x: ")
        ip_cidr_split = ip_addr_and_mask.split("/")
        ip_addr = ip_cidr_split[0]
        cidr = ip_cidr_split[1]
        return ip_addr, cidr
    elif not return_tuple:
        if not regex_ucast_ip_and_mask.match(ip_addr_and_mask):
            return False
        else:
            return True


def ucast_ip(ip_addr, return_tuple=True):
    """
    Function to check if a address is unicast
    Args:
        ip_addr: Unicast IP address in the following format 192.168.1.1
        return_tuple: Set to True it returns a IP, set to False returns True or False

    Returns: see return_tuple for return options

    """
    regex_ucast_ip = __re.compile("^((22[0-3])|(2[0-1][0-9])|(1[0-9][0-9])|([1-9]?[0-9]))\.((25[0-5])|(2[0-4][0-9])|(1[0-9][0-9])|([1-9]?[0-9]))\.((25[0-5])|(2[0-4][0-9])|(1[0-9][0-9])|([1-9]?[0-9]))\.((25[0-5])|(2[0-4][0-9])|(1[0-9][0-9])|([1-9]?[0-9]))$")
    if return_tuple:
        while not regex_ucast_ip.match(ip_addr):
            print("Not a good unicast IP.")
            print("Please try again.")
            ip_addr = input("Please enter a unicast IP address in the following format x.x.x.x: ")
        return ip_addr
    elif not return_tuple:
        if not regex_ucast_ip.match(ip_addr):
            return False
        else:
            return True


def mcast_ip_mask(ip_addr_and_mask, return_tuple=True):
    """
    Function to check if a address is multicast and that the CIDR mask is good
    Args:
        ip_addr_and_mask: Multicast IP address and mask in the following format 239.1.1.1/24
        return_tuple: Set to True it returns a IP and mask in a tuple, set to False returns True or False

    Returns: see return_tuple for return options

    """
    regex_mcast_ip_and_mask = __re.compile("^(((2[2-3][4-9])|(23[0-3]))\.((25[0-5])|(2[0-4][0-9])|(1[0-9][0-9])|([1-9]?[0-9]))\.((25[0-5])|(2[0-4][0-9])|(1[0-9][0-9])|([1-9]?[0-9]))\.((25[0-5])|(2[0-4][0-9])|(1[0-9][0-9])|([1-9]?[0-9]))/((3[0-2])|([1-2][0-9])|[3-9]))$")
    if return_tuple:
        while not regex_mcast_ip_and_mask.match(ip_addr_and_mask):
            print("Not a good multicast IP and CIDR mask combo.")
            print("Please try again.")
            ip_addr_and_mask = input("Please enter a multicast IP address and mask in the follwing format x.x.x.x/x: ")
        ip_cidr_split = ip_addr_and_mask.split("/")
        ip_addr = ip_cidr_split[0]
        cidr = ip_cidr_split[1]
        return ip_addr, cidr
    elif not return_tuple:
        if not regex_mcast_ip_and_mask.match(ip_addr_and_mask):
            return False
        else:
            return True
    

def mcast_ip(ip_addr, return_tuple=True):
    """
    Function to check if a address is multicast
    Args:
        ip_addr: Multicast IP address in the following format 239.1.1.1
        return_tuple: Set to True it returns a IP, set to False returns True or False

    Returns: see return_tuple for return options

    """
    regex_mcast_ip = __re.compile("^(((2[2-3][4-9])|(23[0-3]))\.((25[0-5])|(2[0-4][0-9])|(1[0-9][0-9])|([1-9]?[0-9]))\.((25[0-5])|(2[0-4][0-9])|(1[0-9][0-9])|([1-9]?[0-9]))\.((25[0-5])|(2[0-4][0-9])|(1[0-9][0-9])|([1-9]?[0-9])))$")
    if return_tuple:
        while not regex_mcast_ip.match(ip_addr):
            print("Not a good multicast IP.")
            print("Please try again.")
            ip_addr = input("Please enter a multicast IP address in the following format x.x.x.x: ")
        return ip_addr
    elif not return_tuple:
        if not regex_mcast_ip.match(ip_addr):
            return False
        else:
            return True


def ip_mask(ip_addr_and_mask, return_tuple=True):
    """
    Function to check if a address and CIDR mask is good
    Args:
        ip_addr_and_mask: IP address and mask in the following format 192.168.1.1/24
        return_tuple: Set to True it returns a IP and mask in a tuple, set to False returns True or False

    Returns: see return_tuple for return options

    """
    regex_ip_and_mask = __re.compile("^((25[0-5])|(2[0-4][0-9])|(1[0-9][0-9])|([1-9]?[0-9]))\.((25[0-5])|(2[0-4][0-9])|(1[0-9][0-9])|([1-9]?[0-9]))\.((25[0-5])|(2[0-4][0-9])|(1[0-9][0-9])|([1-9]?[0-9]))\.((25[0-5])|(2[0-4][0-9])|(1[0-9][0-9])|([1-9]?[0-9]))/((3[0-2])|([1-2]?[0-9]))$")
    if return_tuple:
        while not regex_ip_and_mask.match(ip_addr_and_mask):
            print("Not a good IP and CIDR mask combo.")
            print("Please try again.")
            ip_addr_and_mask = input("Please enter a IP address and mask in the follwing format x.x.x.x/x: ")
        ip_cidr_split = ip_addr_and_mask.split("/")
        ip_addr = ip_cidr_split[0]
        cidr = ip_cidr_split[1]
        return ip_addr, cidr
    elif not return_tuple:
        if not regex_ip_and_mask.match(ip_addr_and_mask):
            return False
        else:
            return True


def ip(ip_addr, return_tuple=True):
    """
    Function to check if a address is good
    Args:
        ip_addr: IP address in the following format 192.168.1.1
        return_tuple: Set to True it returns a IP, set to False returns True or False

    Returns: see return_tuple for return options

    """
    regex_ip = __re.compile("^((25[0-5])|(2[0-4][0-9])|(1[0-9][0-9])|([1-9]?[0-9]))\.((25[0-5])|(2[0-4][0-9])|(1[0-9][0-9])|([1-9]?[0-9]))\.((25[0-5])|(2[0-4][0-9])|(1[0-9][0-9])|([1-9]?[0-9]))\.((25[0-5])|(2[0-4][0-9])|(1[0-9][0-9])|([1-9]?[0-9]))$")
    if return_tuple:
        while not regex_ip.match(ip_addr):
            print("Not a good IP.")
            print("Please try again.")
            ip_addr = input("Please enter a IP address in the following format x.x.x.x: ")
        return ip_addr
    elif not return_tuple:
        if not regex_ip.match(ip_addr):
            return False
        else:
            return True


def cidr_check(cidr, return_cidr=True):
    """
    Function to verify a good CIDR value
    Args:
        cidr: CIDR value 0 to 32
        return_cidr: Set to True it returns a CIDR value, set to False returns True or False

    Returns: see return_cidr for return options

    """
    try:
        if int(cidr) < 0 or int(cidr) > 32:
            good_cidr = False
        else:
            good_cidr = True
        if return_cidr:
            while not good_cidr:
                print("Sorry the CIDR value %s is not a valid value must be a value of 0 to 32.  Please try again."
                      % (cidr,))
                cidr = input("What is the mask for in CIDR format?: ")
                if int(cidr) < 0 or int(cidr) > 32:
                    good_cidr = False
                else:
                    good_cidr = True
            return cidr
        elif not return_cidr:
            return good_cidr
    except ValueError:
        LOGGER.critical('Function cidr_check expected a number but got {item}'.format(item=cidr))
        raise ValueError("The input needs to be a number!!")


def get_neighbor_ip(ip_addr, cidr="30"):
    """
    Function to figure out the IP's between neighbors address
    Args:
        ip_addr: Unicast IP address in the following format 192.168.1.1
        cidr: CIDR value of 30, or 31

    Returns: returns Our IP and the Neighbor IP in a tuple

    """
    our_octet = None
    neighbor_octet = None
    try:
        ip_addr_split = ip_addr.split(".")
        max_counter = 0
        if int(cidr) == 30:
            ranger = 4
        elif int(cidr) == 31:
            ranger = 2
        while max_counter < 256:
            try:
                if int(ip_addr_split[3]) >= max_counter and int(ip_addr_split[3]) < (max_counter + ranger):
                    if ranger == 4:
                        our_octet = max_counter + 1
                        neighbor_octet = max_counter + 2
                        break
                    elif ranger == 2:
                        our_octet = max_counter
                        neighbor_octet = max_counter + 1
                        break   
                max_counter += ranger
            except UnboundLocalError:
                print("The mask between the neighbors must be 30, or 31")
                exit("BAD NEIGHBOR MASK")
        if int(ip_addr_split[3]) == our_octet:
            our_ip_addr = "%s.%s.%s.%i" % (ip_addr_split[0], ip_addr_split[1], ip_addr_split[2], our_octet)
            neighbor_ip_addr = "%s.%s.%s.%i" % (ip_addr_split[0], ip_addr_split[1], ip_addr_split[2], neighbor_octet)
        elif int(ip_addr_split[3]) == neighbor_octet:
            neighbor_ip_addr = "%s.%s.%s.%i" % (ip_addr_split[0], ip_addr_split[1], ip_addr_split[2], our_octet)
            our_ip_addr = "%s.%s.%s.%i" % (ip_addr_split[0], ip_addr_split[1], ip_addr_split[2], neighbor_octet)
        else:
            our_ip_addr = "%s.%s.%s.%i" % (ip_addr_split[0], ip_addr_split[1], ip_addr_split[2], our_octet)
            neighbor_ip_addr = "%s.%s.%s.%i" % (ip_addr_split[0], ip_addr_split[1], ip_addr_split[2], neighbor_octet)
        return our_ip_addr, neighbor_ip_addr
    except IndexError:
        LOGGER.critical('Function get_neighbor_ip IndexError ip_addr {item} cidr {cidr}'.format(item=ip_addr,
                                                                                                cidr=cidr))
        raise IndexError("You have entered invalid input, you must enter a ipv4 address")


def whole_subnet_maker(ip_addr, cidr):
    """
    Function to return a whole subnet value from a IP address and CIDR pair
    Args:
        ip_addr: Unicast or Multicast IP address or subnet in the following format 192.168.1.1, 239.1.1.1
        cidr: CIDR value of 0 to 32

    Returns: returns the corrected whole subnet

    """
    if ucast_ip(ip_addr, False) == False and mcast_ip(ip_addr, False) == False:
        LOGGER.critical('Function whole_subnet_maker ip_addr {item}'.format(item=ip_addr))
        raise ValueError("Not a good ipv4 address")
    if not cidr_check(cidr, False):
        LOGGER.critical('Function whole_subnet_maker cidr {item}'.format(item=cidr))
        raise ValueError("Not a good CIDR value should be 0 to 32")

    def subnet_corrector(octet, cidr):
        """ Function to correct a octet for a subnet """
        cidr_int = int(cidr)
        octet_int = int(octet)
        if cidr_int >= 24:
            cidr_int = __mask_conversion[cidr_int]["OCT4"]
        elif cidr_int >= 16:
            cidr_int = __mask_conversion[cidr_int]["OCT3"]
        elif cidr_int >= 8:
            cidr_int = __mask_conversion[cidr_int]["OCT2"]
        elif cidr_int >= 1:
            cidr_int = __mask_conversion[cidr_int]["OCT1"]
        cidr_count = 0
        cidr_v = 256 - cidr_int
        cidr_2 = 256 - cidr_int
        while cidr_count < 300:
            if octet_int >= cidr_count and octet_int <= cidr_2:
                    cidr_int = cidr_count
            cidr_count = cidr_2
            cidr_2 = cidr_2 + cidr_v
        return str(cidr_int)
    ip_addr_split = ip_addr.split(".")
    if int(cidr) >= 24:
        octet = subnet_corrector(ip_addr_split[3], cidr)
        completed = ip_addr_split[0] + "." + ip_addr_split[1] + "." + ip_addr_split[2] + "." + octet
        return completed
    elif int(cidr) >= 16:
        octet = subnet_corrector(ip_addr_split[2], cidr)
        completed = ip_addr_split[0] + "." + ip_addr_split[1] + "." + octet + ".0"
        return completed
    elif int(cidr) >= 8:
        octet = subnet_corrector(ip_addr_split[1], cidr)
        completed = ip_addr_split[0] + "." + octet + ".0.0"
        return completed
    elif int(cidr) >= 1:
        octet = subnet_corrector(ip_addr_split[0], cidr)
        completed = octet + ".0.0.0"
        return completed
    else:
        return "0.0.0.0"


def subnet_range(ip_net, cidr):
    """
    Function to return a subnet range value from a IP address and CIDR pair
    Args:
        ip_net: Unicast or Multicast IP address or subnet in the following format 192.168.1.1, 239.1.1.1
        cidr: CIDR value of 1 to 32

    Returns: returns a dictionary of info

    """
    subnets_dict = dict()
    subnet = whole_subnet_maker(ip_net, cidr)
    subnets_dict['IP'] = ip_net
    subnets_dict['NET'] = subnet
    subnets_dict['CIDR'] = '%s/%s' % (whole_subnet_maker(ip_net, cidr), cidr)
    if int(cidr) >= 24:
        subnet_split = subnet.split('.')
        first_ip = int(subnet_split[3]) + 1
        last_ip = (int(subnet_split[3]) + 1) + (253 - int(__mask_conversion[int(cidr)]['OCT4']))
        bcast_ip = (int(subnet_split[3]) + 1) + (254 - int(__mask_conversion[int(cidr)]['OCT4']))
        temp = '%s.%s.%s.' % (subnet_split[0], subnet_split[1], subnet_split[2])
        subnets_dict['RANGE'] = '%s%i to %s%i' % (temp, first_ip, temp, last_ip)
        subnets_dict['BCAST'] = '%s%i' % (temp, bcast_ip)
        subnets_dict['MASK'] = __mask_conversion[int(cidr)]['MASK']
        subnets_dict['INVMASK'] = __mask_conversion[int(cidr)]['INVMASK']
        subnets_dict['CIDRVAL'] = __mask_conversion[int(cidr)]['CIDR']
    elif int(cidr) >= 16:
        subnet_split = subnet.split('.')
        first_ip = int(subnet_split[2])
        last_ip = (int(subnet_split[2]) + 1) + (254 - int(__mask_conversion[int(cidr)]['OCT3']))
        bcast_ip = (int(subnet_split[2]) + 1) + (254 - int(__mask_conversion[int(cidr)]['OCT3']))
        temp = '%s.%s.' % (subnet_split[0], subnet_split[1])
        subnets_dict['RANGE'] = '%s%i.1 to %s%i.254' % (temp, first_ip, temp, last_ip)
        subnets_dict['BCAST'] = '%s%i.255' % (temp, bcast_ip)
        subnets_dict['MASK'] = __mask_conversion[int(cidr)]['MASK']
        subnets_dict['INVMASK'] = __mask_conversion[int(cidr)]['INVMASK']
        subnets_dict['CIDRVAL'] = __mask_conversion[int(cidr)]['CIDR']
    elif int(cidr) >= 8:
        subnet_split = subnet.split('.')
        first_ip = int(subnet_split[1])
        last_ip = (int(subnet_split[1]) + 1) + (254 - int(__mask_conversion[int(cidr)]['OCT2']))
        bcast_ip = (int(subnet_split[1]) + 1) + (254 - int(__mask_conversion[int(cidr)]['OCT2']))
        temp = '%s.' % (subnet_split[0],)
        subnets_dict['RANGE'] = '%s%i.0.1 to %s%i.255.254' % (temp, first_ip, temp, last_ip)
        subnets_dict['BCAST'] = '%s%i.255.255' % (temp, bcast_ip)
        subnets_dict['MASK'] = __mask_conversion[int(cidr)]['MASK']
        subnets_dict['INVMASK'] = __mask_conversion[int(cidr)]['INVMASK']
        subnets_dict['CIDRVAL'] = __mask_conversion[int(cidr)]['CIDR']
    elif int(cidr) >= 1:
        subnet_split = subnet.split('.')
        first_ip = int(subnet_split[0])
        last_ip = (int(subnet_split[0]) + 1) + (254 - int(__mask_conversion[int(cidr)]['OCT1']))
        bcast_ip = (int(subnet_split[0]) + 1) + (254 - int(__mask_conversion[int(cidr)]['OCT1']))
        subnets_dict['RANGE'] = '%i.0.0.1 to %i.255.255.254' % (first_ip, last_ip)
        subnets_dict['BCAST'] = '%i.255.255.255' % (bcast_ip,)
        subnets_dict['MASK'] = __mask_conversion[int(cidr)]['MASK']
        subnets_dict['INVMASK'] = __mask_conversion[int(cidr)]['INVMASK']
        subnets_dict['CIDRVAL'] = __mask_conversion[int(cidr)]['CIDR']
    return subnets_dict


def all_subnets_possible(ip_net, cidr):
    """
    Function to return every subnet a ip can belong to with a longer prefix
    Args:
        ip_net: Unicast or Multicast IP address or subnet in the following format 192.168.1.1, 239.1.1.1
        cidr: CIDR value of 0 to 32

    Returns: returns a list of subnets

    """
    return all_subnets_longer_prefix(ip_net, cidr)


def all_subnets_longer_prefix(ip_net, cidr):
    """
    Function to return every subnet a ip can belong to with a longer prefix
    Args:
        ip_net: Unicast or Multicast IP address or subnet in the following format 192.168.1.1, 239.1.1.1
        cidr: CIDR value of 0 to 32

    Returns: returns a list of subnets

    """
    subnets_list = list()
    while int(cidr) <= 32:
        try:
            subnets_list.append('%s/%s' % (whole_subnet_maker(ip_net, cidr), cidr))
        except Exception as e:
            LOGGER.critical('Function all_subnets_longer_prefix {item}'.format(item=e))
            pass
        cidr = str(int(cidr) + 1)
    return subnets_list


def all_subnets_shorter_prefix(ip_net, cidr, include_default=False):
    """
    Function to return every subnet a ip can belong to with a shorter prefix
    Args:
        ip_net: Unicast or Multicast IP address or subnet in the following format 192.168.1.1, 239.1.1.1
        cidr: CIDR value of 0 to 32
        include_default: If you want the list to inlclude the default route set to True

    Returns: returns a list of subnets

    """
    subnets_list = list()
    if include_default:
        while int(cidr) >= 0:
            try:
                subnets_list.append('%s/%s' % (whole_subnet_maker(ip_net, cidr), cidr))
            except Exception as e:
                LOGGER.critical('Function all_subnets_shorter_prefix {item}'.format(item=e))
            cidr = str(int(cidr) - 1)
    else:
        while int(cidr) > 0:
            try:
                subnets_list.append('%s/%s' % (whole_subnet_maker(ip_net, cidr), cidr))
            except Exception as e:
                LOGGER.critical('Function all_subnets_shorter_prefix {item}'.format(item=e))
            cidr = str(int(cidr) - 1)
    return subnets_list


def all_ip_address_in_subnet(ip_net, cidr):
    """
    Function to return every ip in a subnet
    :param ip_net: Unicast or Multicast IP address or subnet in the following format 192.168.1.1, 239.1.1.1
    :param cidr: CIDR value of 0 to 32
    :return: 
        A list of ip address's
    
    """
    ip_address_list = list()
    if not ip_mask('{ip_net}/{cidr}'.format(ip_net=ip_net, cidr=cidr), return_tuple=False):
        LOGGER.critical('{network} is not a valid IPv4 network'.format(network='{ip_net}/{cidr}'.format(ip_net=ip_net,
                                                                                                        cidr=cidr)))
        raise ValueError('{network} is not a valid IPv4 network'.format(network='{ip_net}/{cidr}'.format(ip_net=ip_net,
                                                                                                         cidr=cidr)))

    else:
        ip_net = whole_subnet_maker(ip_net, cidr)
        net = __ipaddress.ip_network('{ip_net}/{cidr}'.format(ip_net=ip_net, cidr=cidr))
        for single_ip in net:
            ip_address_list.append(str(single_ip))

        return ip_address_list


def number_check(check, return_number=True):
    """
    Function to verify item entered is a number
    Args:
        check: Thing to check for a number
        return_number: Set to True it returns a number value, set to False returns True or False

    Returns: Check return_number for return options

    """
    try:
        int(check)
        good = True
    except ValueError:
        LOGGER.critical('Function number_check ValueError {item}'.format(item=check))
        good = False
    if return_number:
        while not good:
            print("That is not a number.")
            print("Please try again.")
            check = input("Please enter a number?: ")
            try:
                int(check)
                good = True
            except ValueError:
                LOGGER.critical('Function number_check ValueError {item}'.format(item=check))
                good = False
        return check
    else:
        return good


def random_cidr_mask(lowest_mask=16):
    """
    Function to generate a random CIDR value
    :param 
        lowest_mask: An integer value for the lowest mask you want it to generate
    
    :return: 
        A string of a random CIDR mask
        
    """
    if lowest_mask < 33:
        return str(__random.randrange(lowest_mask, 33))

    else:
        LOGGER.critical('{lowest_mask} must be 32 or less.'.format(lowest_mask=lowest_mask))
        raise ValueError('{lowest_mask} must be 32 or less.'.format(lowest_mask=lowest_mask))


def random_ucast_ip():
    """
    Function to generate a random unicast ip address
    :return: 
        A unicast IP Address
    
    """
    first_octet = str(__random.randrange(1, 224))

    def get_other_octetes():
        return str(__random.randrange(0, 255))

    return '{first_octet}.{second_octet}.{third_octet}.{fourth_octet}'.format(first_octet=first_octet,
                                                                              second_octet=get_other_octetes(),
                                                                              third_octet=get_other_octetes(),
                                                                              fourth_octet=get_other_octetes())


def random_mcast_ip():
    """
    Function to generate a random multicast ip address
    :return: 
        A multicast IP Address

    """
    first_octet = str(__random.randrange(224, 240))

    def get_other_octetes():
        return str(__random.randrange(0, 255))

    return '{first_octet}.{second_octet}.{third_octet}.{fourth_octet}'.format(first_octet=first_octet,
                                                                              second_octet=get_other_octetes(),
                                                                              third_octet=get_other_octetes(),
                                                                              fourth_octet=get_other_octetes())


def random_ucast_ip_mask(lowest_mask=16):
    """
    Function to generate a random unicast ip address and cidr mask pair in the following format X.X.X.X/X
    :param 
        lowest_mask: An integer value for the lowest mask you want it to generate
        
    :return: 
        A unicast IP Address and CIDR pair in the following format X.X.X.X/X
        
    """
    return '{ip_addr}/{cidr}'.format(ip_addr=random_ucast_ip(), cidr=random_cidr_mask(lowest_mask))


def random_mcast_ip_mask(lowest_mask=16):
    """
    Function to generate a random multicast ip address and cidr mask pair in the following format X.X.X.X/X
    :param 
        lowest_mask: An integer value for the lowest mask you want it to generate

    :return: 
        A multicast IP Address and CIDR pair in the following format X.X.X.X/X

    """
    return '{ip_addr}/{cidr}'.format(ip_addr=random_mcast_ip(), cidr=random_cidr_mask(lowest_mask))

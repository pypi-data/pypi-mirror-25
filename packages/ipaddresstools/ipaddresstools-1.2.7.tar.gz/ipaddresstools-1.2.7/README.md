# Python Script: ipaddresstools

## Written By: Benjamin P. Trachtenberg 

### Contact Information:  e_ben_75-python@yahoo.com
### If you have any questions e-mail me

### LinkedIn: [Ben Trachtenberg](https://www.linkedin.com/in/ben-trachtenberg-3a78496)
### Docker Hub: [Docker Hub](https://hub.docker.com/r/btr1975)
### PyPi Page for [ipaddresstools](https://pypi.python.org/pypi/ipaddresstools)

### Requirements

* Nothing Specific, I would suggest Python 3.3 and above.

### Installation

* From source "setup.py install"
* From pip "pip install ipaddresstools"

### Languages

* Python

### About

This is a library used to verify, and correct ipv4 address's, and subnets.  I wrote it before a good library was out there for network engineers.

### Functions included in v1.0.0
* ucast_ip_mask(ip_addr_and_mask, return_tuple=True)
* ucast_ip(ip_addr, return_tuple=True)
* mcast_ip_mask(ip_addr_and_mask, return_tuple=True)
* mcast_ip(ip_addr, return_tuple=True)
* cidr_check(cidr, return_cidr=True)
* get_neighbor_ip(ip_addr, cidr="30")
* whole_subnet_maker (ip_addr, cidr)

### Functions Added in v1.1.0
* number_check(check, return_number=True)

### Functions Added in v1.1.1
* subnet_range(ip_net, cidr)
* all_subnets_possible(ip_net, cidr)

### Functions Added in v1.1.2
* all_subnets_longer_prefix(ip_net, cidr)
* all_subnets_shorter_prefix(ip_net, cidr, include_default=False)
* all_subnets_possible(ip_net, cidr) = AllSubnetsPossibleLongerPrefix(strIpNet,strCidr)

### Functions Added in v1.2.1
* ip_mask(ip_addr_and_mask, return_tuple=True):
* ip(ip_addr, return_tuple=True):

### Functions Added to v1.2.3
* mask_conversion = __mask_conversion

### Functions Added to v1.2.4
* all_ip_address_in_subnet(ip_net, cidr)

### Functions Added to v1.2.5
* random_cidr_mask(lowest_mask=16)
* random_ucast_ip()
* random_mcast_ip()
* random_ucast_ip_mask(lowest_mask=16)
* random_mcast_ip_mask(lowest_mask=16)

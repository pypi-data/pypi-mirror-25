Python Script: ipaddresstools
=============================

Written By: Benjamin P. Trachtenberg
------------------------------------

Contact Information: e\_ben\_75-python@yahoo.com
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have any questions e-mail me
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

LinkedIn: `Ben Trachtenberg <https://www.linkedin.com/in/ben-trachtenberg-3a78496>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Docker Hub: `Docker Hub <https://hub.docker.com/r/btr1975>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Requirements
~~~~~~~~~~~~

-  Nothing Specific, I would suggest Python 3.3 and above.

Languages
~~~~~~~~~

-  Python

About
~~~~~

This is a library used to verify, and correct ipv4 address's, and
subnets. I wrote it before a good library was out there for network
engineers.

Functions included in v1.0.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  ucast\_ip\_mask(ip\_addr\_and\_mask, return\_tuple=True)
-  ucast\_ip(ip\_addr, return\_tuple=True)
-  mcast\_ip\_mask(ip\_addr\_and\_mask, return\_tuple=True)
-  mcast\_ip(ip\_addr, return\_tuple=True)
-  cidr\_check(cidr, return\_cidr=True)
-  get\_neighbor\_ip(ip\_addr, cidr="30")
-  whole\_subnet\_maker (ip\_addr, cidr)

Functions Added in v1.1.0
~~~~~~~~~~~~~~~~~~~~~~~~~

-  number\_check(check, return\_number=True)

Functions Added in v1.1.1
~~~~~~~~~~~~~~~~~~~~~~~~~

-  subnet\_range(ip\_net, cidr)
-  all\_subnets\_possible(ip\_net, cidr)

Functions Added in v1.1.2
~~~~~~~~~~~~~~~~~~~~~~~~~

-  all\_subnets\_longer\_prefix(ip\_net, cidr)
-  all\_subnets\_shorter\_prefix(ip\_net, cidr, include\_default=False)
-  all\_subnets\_possible(ip\_net, cidr) =
   AllSubnetsPossibleLongerPrefix(strIpNet,strCidr)

Functions Added in v1.2.1
~~~~~~~~~~~~~~~~~~~~~~~~~

-  ip\_mask(ip\_addr\_and\_mask, return\_tuple=True):
-  ip(ip\_addr, return\_tuple=True):

Functions Added to v1.2.3
~~~~~~~~~~~~~~~~~~~~~~~~~

-  mask\_conversion = \_\_mask\_conversion

Functions Added to v1.2.4
~~~~~~~~~~~~~~~~~~~~~~~~~

-  all\_ip\_address\_in\_subnet(ip\_net, cidr)

Functions Added to v1.2.5
~~~~~~~~~~~~~~~~~~~~~~~~~

-  random\_cidr\_mask(lowest\_mask=16)
-  random\_ucast\_ip()
-  random\_mcast\_ip()
-  random\_ucast\_ip\_mask(lowest\_mask=16)
-  random\_mcast\_ip\_mask(lowest\_mask=16)

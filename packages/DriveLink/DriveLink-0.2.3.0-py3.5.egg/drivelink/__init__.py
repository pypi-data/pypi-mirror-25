"""
.. moduleauthor:: Chris Dusold <DriveLink@chrisdusold.com>

A library containing storage classes that maintain small RAM usage and original structure access order.

The motivation for this module was to provide constant size RAM usage
while maintaining normal use of Python Dictionaries and possibly other
structures for semi-big data, where it isn't large enough to warrant more
big data centric solutions.

More importantly, this library intends to preserve the usability of Python for rapid
prototyping, while enabling larger data access.

"""
from drivelink._disklink import Link
from drivelink._diskdict import Dict
from drivelink._disklist import List
from drivelink._diskmemoize import cached
from drivelink._ordereddiskdict import OrderedDict

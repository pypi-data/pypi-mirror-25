"""
.. moduleauthor:: Chris Dusold <DriveLink@chrisdusold.com>

A module containing general purpose, cross instance hashing.

This module intends to make storage and cache checking stable accross instances.

"""
from drivelink.hash._hasher import hash
from drivelink.hash._hasher import frozen_hash
from drivelink.hash._hasher import Deterministic_Hashable

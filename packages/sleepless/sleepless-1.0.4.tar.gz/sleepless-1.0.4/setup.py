#!/usr/bin/python -OO
# Copyright 2008-2017 The SABnzbd-Team <team@sabnzbd.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


from setuptools import setup, Extension


sleepless = Extension('sleepless',
                      sources = ['sleepless.c', 'sleeplesspy.c'],
                      extra_link_args = ['-framework', 'CoreFoundation',
                                         '-framework', 'ApplicationServices',
                                         '-framework', 'Cocoa']
                     )

setup(
    name            = "sleepless",
    version         = "1.0.4",
    author          = "SABnzbd",
    author_email    = "team@sabnzbd.org",
    url             = "https://github.com/sabnzbd/sabbuild",
    license         = "LGPLv3",
    ext_modules     = [sleepless],
    classifiers     = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: C",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: MacOS",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Plugins",
        "Environment :: MacOS X",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Power (UPS)"
    ],
    description     = "Keep macOS (OSX) awake by setting power assertions",
    long_description = """
sleepless
------------

Python wrapper around the macOS (OSX) assertion for preventing standby "due to lack of user action".

Usage:
------------

.. code:: python

    import sleepless

    # Tell OS to keep awake
    sleepless.keep_awake(u"MyApp - why I don't sleep")

    # Do stuff
    do_lengthy_action()

    # Calling again is harmless
    sleepless.keep_awake(u"MyApp - why I don't sleep")

    # When done
    sleepless.allow_sleep()


2012 The SABnzbd Team <team@sabnzbd.org>
"""
)
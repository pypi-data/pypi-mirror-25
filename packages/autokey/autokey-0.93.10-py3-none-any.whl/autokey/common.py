#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 Chris Dekter
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os, dbus.service

CONFIG_DIR = os.path.join(os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config')), "autokey")
LOCK_FILE = CONFIG_DIR + "/autokey.pid"
LOG_FILE = CONFIG_DIR + "/autokey.log"
MAX_LOG_SIZE = 5 * 1024 * 1024 # 5 megabytes
MAX_LOG_COUNT = 3
LOG_FORMAT = "%(asctime)s %(levelname)s - %(name)s - %(message)s"

APP_NAME = "autokey"
CATALOG = ""
VERSION = "0.93.10"
HOMEPAGE  = "https://github.com/autokey-py3/autokey"
AUTHOR = 'Chris Dekter'
AUTHOR_EMAIL = 'cdekter@gmail.com'
MAINTAINER = 'GuoCi'
MAINTAINER_EMAIL = 'guociz@gmail.com'
BUG_EMAIL = "guociz@gmail.com"

FAQ_URL = "https://github.com/autokey-py3/autokey-py3/wiki/FAQ"
API_URL = "https://autokey-py3.github.io/"
HELP_URL = "https://github.com/autokey-py3/autokey-py3/wiki/Troubleshooting"
BUG_URL = HOMEPAGE + "/issues"

ICON_FILE = "autokey"
ICON_FILE_NOTIFICATION = "autokey-status"
ICON_FILE_NOTIFICATION_DARK = "autokey-status-dark"
ICON_FILE_NOTIFICATION_ERROR = "autokey-status-error"

USING_QT = False

class AppService(dbus.service.Object):

    def __init__(self, app):
        busName = dbus.service.BusName('org.autokey.Service', bus=dbus.SessionBus())
        dbus.service.Object.__init__(self, busName, "/AppService")
        self.app = app

    @dbus.service.method(dbus_interface='org.autokey.Service', in_signature='', out_signature='')
    def show_configure(self):
        self.app.show_configure()

    @dbus.service.method(dbus_interface='org.autokey.Service', in_signature='s', out_signature='')
    def run_script(self, name):
        self.app.service.run_script(name)

    @dbus.service.method(dbus_interface='org.autokey.Service', in_signature='s', out_signature='')
    def run_phrase(self, name):
        self.app.service.run_phrase(name)

    @dbus.service.method(dbus_interface='org.autokey.Service', in_signature='s', out_signature='')
    def run_folder(self, name):
        self.app.service.run_folder(name)

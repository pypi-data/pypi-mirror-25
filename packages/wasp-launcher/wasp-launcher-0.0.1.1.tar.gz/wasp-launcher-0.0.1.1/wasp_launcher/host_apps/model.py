# -*- coding: utf-8 -*-
# wasp_launcher/host_apps/model.py
#
# Copyright (C) 2016 the wasp-launcher authors and contributors
# <see AUTHORS file>
#
# This file is part of wasp-launcher.
#
# Wasp-launcher is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Wasp-launcher is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with wasp-launcher.  If not, see <http://www.gnu.org/licenses/>.

# TODO: document the code
# TODO: write tests for the code
# TODO: do smthng with WHostAppModelStorage

# noinspection PyUnresolvedReferences
from wasp_launcher.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
# noinspection PyUnresolvedReferences
from wasp_launcher.version import __status__

from wasp_launcher.apps import WSyncHostApp, WAppsGlobals


class WHostAppModelStorage:
	pass


class WGuestModelLoadApp(WSyncHostApp):

	__registry_tag__ = 'com.binblob.wasp-launcher.host-app.model-load'

	__dependency__ = [
		'com.binblob.wasp-launcher.host-app.guest-apps'
	]

	def start(self):
		WAppsGlobals.models = WHostAppModelStorage()

	def stop(self):
		WAppsGlobals.models = None

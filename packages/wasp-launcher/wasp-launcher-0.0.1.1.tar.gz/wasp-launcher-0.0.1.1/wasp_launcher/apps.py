# -*- coding: utf-8 -*-
# wasp_launcher/guest_apps.py
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
# TODO: test the code

# noinspection PyUnresolvedReferences
from wasp_launcher.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
# noinspection PyUnresolvedReferences
from wasp_launcher.version import __status__

import traceback

from abc import ABCMeta, abstractmethod, abstractclassmethod

from wasp_general.verify import verify_type, verify_value

from wasp_general.task.dependency import WDependentTask
from wasp_general.task.base import WTask, WSyncTask
from wasp_general.task.thread import WThreadTask
from wasp_general.task.dependency import WTaskDependencyRegistry, WTaskDependencyRegistryStorage
from wasp_general.command.enhanced import WEnhancedCommand

from wasp_general.network.web.service import WWebService, WWebTargetRoute, WWebEnhancedPresenter
from wasp_general.network.web.proto import WWebRequestProto
from wasp_general.network.web.template import WWebTemplateResponse


class WThreadTaskLoggingHandler:

	def thread_exception(self, raised_exception):
		if WAppsGlobals.log is not None:
			msg = 'Thread execution was stopped by the exception. Exception: %s' % str(raised_exception)
			WAppsGlobals.log.error(msg)
			WAppsGlobals.log.error('Traceback:\n' + traceback.format_exc())
		else:
			WThreadTask.thread_exception(self, raised_exception)


class WHostAppRegistry(WTaskDependencyRegistry):
	""" Main registry to keep host applications
	"""
	__registry_storage__ = WTaskDependencyRegistryStorage()
	""" Default storage for this type of registry
	"""


class WRegisteredHostApp(WTask, metaclass=WDependentTask):
	""" Base class for registered host apps, such application maintains core functionality and creates environment
	for guest application to work. This class defines link to the registry, which holds every host app.
	"""

	__registry__ = WHostAppRegistry
	""" Link to registry
	"""


class WSyncHostApp(WRegisteredHostApp, WSyncTask, metaclass=WDependentTask):
	""" Host application, that executes in foreground
	"""
	pass


class WThreadedHostApp(WRegisteredHostApp, WThreadTaskLoggingHandler, WThreadTask, metaclass=WDependentTask):
	""" Host application, that executes in a separate thread
	"""
	pass


class WBrokerCommand(WEnhancedCommand):

	@abstractmethod
	def brief_description(self):
		raise NotImplementedError('This method is abstract')

	def detailed_description(self):
		help = 'This is help information for "%s" command (%s). ' % (self.command(), self.brief_description())

		arguments_help = self.arguments_help()
		if len(arguments_help) == 0:
			help += 'Command does not have arguments\n'
		else:
			help += 'Command arguments:\n'
			for argument_name, argument_description in arguments_help:
				help += '\t%s - %s\n' % (argument_name, argument_description)
		return help


class WCommandKit(metaclass=ABCMeta):

	@abstractclassmethod
	def brief_description(self):
		"""

		:return: str
		"""
		raise NotImplementedError('This method is abstract')

	@abstractclassmethod
	def commands(self):
		"""

		:return: WCommand
		"""
		raise NotImplementedError('This method is abstract')


class WHostAppCommandKit(WRegisteredHostApp, WCommandKit):

	@classmethod
	def name(cls):
		return cls.__registry_tag__


class WGuestAppRegistry(WTaskDependencyRegistry):
	__registry_storage__ = WTaskDependencyRegistryStorage()


class WAppsGlobals:
	""" Storage of global variables, that are widely used across all application
	"""

	log = None
	""" Application logger (logging.Logger instance. See :class:`wasp_launcher.host_apps.log.WLauncherLogSetupApp`)
	"""

	config = None
	""" Current server configuration (wasp_general.config.WConfig instance.
	See :class:`wasp_launcher.host_apps.config.WLauncherConfigApp`)
	"""

	apps_registry = WGuestAppRegistry
	started_apps = []
	templates = None

	models = None

	wasp_web_service = None
	tornado_io_loop = None
	tornado_service = None

	broker_commands = None
	""" Brokers management commands
	"""

	scheduler = None


class WGuestApp(WSyncTask, metaclass=WDependentTask):

	__auto_registry__ = False

	@classmethod
	def name(cls):
		return cls.__registry_tag__

	@classmethod
	def description(cls):
		return None


class WGuestWebPresenter(WWebEnhancedPresenter, metaclass=ABCMeta):

	@verify_type('paranoid', request=WWebRequestProto, target_route=WWebTargetRoute, service=WWebService)
	def __init__(self, request, target_route, service):
		WWebEnhancedPresenter.__init__(self, request, target_route, service)
		self._context = {}

	@verify_type('paranoid', template_id=str)
	@verify_value('paranoid', template_id=lambda x: len(x) > 0)
	def __template__(self, template_id):
		return WAppsGlobals.templates.lookup(template_id)

	@verify_type('paranoid', template_id=str)
	@verify_value('paranoid', template_id=lambda x: len(x) > 0)
	def __template_response__(self, template_id):
		return WWebTemplateResponse(self.__template__(template_id), context=self._context)


class WGuestWebApp(WGuestApp):

	@classmethod
	def public_presenters(cls):
		return tuple()

	@classmethod
	def public_routes(cls):
		""" Return routes which are published by an application

		:return: tuple of WWebRoute
		"""
		return tuple()

	@classmethod
	def template_path(cls):
		'''

		can be none or non-existens path

		:return:
		'''
		return None

	@classmethod
	def py_templates_package(cls):
		return None

	@classmethod
	def static_files_path(cls):
		'''

		can be none or non-existens path

		:return:
		'''
		return None

	def start(self):
		for presenter in self.public_presenters():
			WAppsGlobals.wasp_web_service.add_presenter(presenter)
			WAppsGlobals.log.info(
				'Presenter "%s" was added to the web service registry' % presenter.__presenter_name__()
			)
		for route in self.public_routes():
			WAppsGlobals.wasp_web_service.route_map().append(route)

	def stop(self):
		pass


class WGuestModelApp(WGuestApp):

	def start(self):
		pass

	def stop(self):
		pass


class WGuestAppCommandKit(WGuestApp, WCommandKit):

	def start(self):
		WAppsGlobals.broker_commands.add_guest_app(self)

	def stop(self):
		pass

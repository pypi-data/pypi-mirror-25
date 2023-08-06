# -*- coding: utf-8 -*-
# service_hooks.py
# Copyright (C) 2016 LEAP
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
"""
Hooks for service composition.
"""
from collections import defaultdict

from twisted.application.service import IService, Service
from twisted.python import log

from zope.interface import implementer


@implementer(IService)
class HookableService(Service):

    """
    This service allows for other services in a Twisted Service tree to be
    notified whenever a certain kind of hook is triggered.

    During the service composition, one is expected to register
    a hook name with the name of the service that wants to react to the
    triggering of the hook. All the services, both hooked and listeners, should
    be registered against the same parent service.

    Upon the hook being triggered, the method "hook_<name>" will be called with
    the passed data in the listener service.
    """

    def register_hook(self, name, listener):
        if not hasattr(self, 'event_listeners'):
            self.event_listeners = defaultdict(list)
        log.msg("Registering hook %s->%s" % (name, listener))
        self.event_listeners[name].append(listener)

    def trigger_hook(self, name, **data):

        def react_to_hook(listener, name, **kw):
            try:
                getattr(listener, 'hook_' + name)(**kw)
            except AttributeError:
                raise RuntimeError(
                    "Tried to notify a hook, but the listener service class %s"
                    "has not defined the proper method" % listener.__class__)

        if not hasattr(self, 'event_listeners'):
            self.event_listeners = defaultdict(list)
        listeners = self._get_listener_services(name)

        for listener in listeners:
            react_to_hook(listener, name, **data)

    def _get_sibling_service(self, name):
        return self.parent.getServiceNamed(name)

    def _get_listener_services(self, hook):
        if hook in self.event_listeners:
            service_names = self.event_listeners[hook]
            services = [
                self._get_sibling_service(name) for name in service_names]
            return services


from flask import Flask
from edmunds.foundation.concerns.config import Config as ConcernsConfig
from edmunds.foundation.concerns.runtimeenvironment import RuntimeEnvironment as ConcernsRuntimeEnvironment
from edmunds.foundation.concerns.serviceproviders import ServiceProviders as ConcernsServiceProviders
from edmunds.foundation.concerns.middleware import Middleware as ConcernsMiddleware
from edmunds.foundation.concerns.requestrouting import RequestRouting as ConcernsRequestRouting
from edmunds.foundation.concerns.storage import Storage as ConcernsStorage
from edmunds.foundation.concerns.session import Session as ConcernsSession
from edmunds.foundation.concerns.database import Database as ConcernsDatabase
from edmunds.foundation.concerns.localization import Localization as ConcernsLocalization
from edmunds.foundation.concerns.cache import Cache as ConcernsCache
from edmunds.exceptions.exceptionsserviceprovider import ExceptionsServiceProvider
from edmunds.log.providers.logserviceprovider import LogServiceProvider
from edmunds.session.providers.sessionserviceprovider import SessionServiceProvider
from edmunds.storage.providers.storageserviceprovider import StorageServiceProvider
from edmunds.database.providers.databaseserviceprovider import DatabaseServiceProvider
from edmunds.localization.providers.localizationserviceprovider import LocalizationServiceProvider
from edmunds.cache.providers.cacheserviceprovider import CacheServiceProvider
from edmunds.http.providers.httpserviceprovider import HttpServiceProvider
from edmunds.config.config import Config
from edmunds.http.request import Request
from edmunds.http.response import Response
from threading import Lock


class Application(Flask,
                  ConcernsConfig,
                  ConcernsRuntimeEnvironment,
                  ConcernsServiceProviders,
                  ConcernsMiddleware,
                  ConcernsRequestRouting,
                  ConcernsStorage,
                  ConcernsSession,
                  ConcernsDatabase,
                  ConcernsLocalization,
                  ConcernsCache):
    """
    The Edmunds Application
    """

    request_class = Request
    response_class = Response
    config_class = Config
    _logger_lock = Lock()

    def __init__(self, import_name, config_dirs=None):
        """
        Initialize the application
        :param import_name:     Import name
        :type  import_name:     str
        :param config_dirs:     Configuration directories
        :type  config_dirs:     list
        """

        super(Application, self).__init__(import_name)

        self.logger_name = 'edmunds.%s' % import_name

        self._init_config(config_dirs)
        self._init_service_providers()
        self._init_middleware()
        self._init_request_routing()
        self._init_runtime_environment()
        self._init_database()

        self.register(HttpServiceProvider)
        self.register(StorageServiceProvider)
        self.register(ExceptionsServiceProvider)
        self.register(LogServiceProvider)
        self.register(SessionServiceProvider)
        self.register(DatabaseServiceProvider)
        self.register(CacheServiceProvider)
        self.register(LocalizationServiceProvider)

    def route(self, rule, **options):
        """
        Register a route
        This is merely a step to abstract the middleware from the route
        :param rule:    The rule for routing the request
        :type  rule:    str
        :param options: List of options
        :type  options: list
        :return:        Decorator function
        :rtype:         function
        """

        # Pre handline
        self._pre_handle_route_dispatching(rule, options)
        self._pre_handle_route_middleware(rule, options)

        # Fetch the decorator function
        decorator = super(Application, self).route(rule, **options)

        # Post handline
        decorator = self._post_handle_route_middleware(decorator, rule, options)
        decorator = self._post_handle_route_dispatching(decorator, rule, options)

        return decorator


from edmunds.foundation.debugmiddleware import DebugMiddleware
from edmunds.profiler.providers.profilerserviceprovider import ProfilerServiceProvider
from edmunds.gae.runtimeenvironment import RuntimeEnvironment as GaeRuntimeEnvironment


class RuntimeEnvironment(object):
    """
    This class concerns runtime-environment code for Application to extend from
    """

    def _init_runtime_environment(self):
        """
        Initialise concerning runtime environment
        """

        # Debug environment
        if self.config('app.debug'):
            self.middleware(DebugMiddleware)

            if self.config('app.profiler.enabled', False):
                self.register(ProfilerServiceProvider)

        # Testing environment
        if self.is_testing():
            self.testing = True

    def environment(self, matches=None):
        """
        Get the environment
        :param matches:     Environment to match with
        :type  matches:     str
        :return:            The environment or checks the given environment
        :rtype:             str|boolean
        """

        environment = self.config['APP_ENV']

        if matches is None:
            return environment
        else:
            return environment == matches

    def is_local(self):
        """
        Check if running in local environment
        """

        return self.environment('local')

    def is_testing(self):
        """
        Check if running in testing environment
        """

        return self.environment('testing')

    def is_production(self):
        """
        Check if running in production environment
        """

        return self.environment('production')

    def is_gae(self):
        """
        Check if running in Google App Engine
        """

        if not hasattr(self, '_is_gae'):
            self._is_gae = GaeRuntimeEnvironment().is_gae()

        return self._is_gae

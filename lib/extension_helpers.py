import os
from build_pack_utils import utils


class PHPExtensionHelper(object):
    """A helper class for making extensions to the cf-php-build-pack"""

    def __init__(self, ctx):
        self._ctx = ctx
        self._services = self._ctx.get('VCAP_SERVICES', {})
        self._application = self._ctx.get('VCAP_APPLICATION', {})
        self._merge_defaults()
        self._php_ini = utils.ConfigFileEditor(
            os.path.join(ctx['BUILD_DIR'], 'php', 'etc', 'php.ini'))
        self._php_fpm = utils.ConfigFileEditor(
            os.path.join(ctx['BUILD_DIR'], 'php', 'etc', 'php-fpm.conf'))
        self._php_api = self._get_api()

    def _get_api(self):
        if self._ctx['PHP_VERSION'].startswith('5.4'):
            return '20100525'
        elif self._ctx['PHP_VERSION'].startswith('5.5'):
            return '20121212'
        elif self._ctx['PHP_VERSION'].startswith('5.6'):
            return '20131226'

    def _merge_defaults(self):
        for key, val in self.defaults().iteritems():
            if key not in self._ctx:
                self._ctx[key] = val

    def defaults(self):
        """Returns a set of default environment variables.

        Create and return a list of default environment variables.  These
        are merged with the build pack context when this the extension
        object is created.

        Return a dictionary.
        """
        return {}

    def should_install(self):
        """Determines if the extension should install it's payload.

        This check is called during the `compile` method of the extension.
        It should return true if the payload of this extension should
        be installed (i.e. the `install` method is called).
        """
        return False

    def should_configure(self):
        """Determines if the extension should configure itself.

        This check is called during the `configure` method of the
        extension.  It should return true if the extension should
        configure itself (i.e. the `configure` method is called).
        """
        return self.should_install()

    def install(self, installer):
        """Install the payload of this extension.

        Called when `should_install` returns true.  This is responsible
        for installing the payload of the extension.

        The argument is the installer object that is passed into the
        `compile` method.
        """
        pass

    def configure(self):
        """Configure the extension.

        Called when `should_configure` returns true.  This method is
        corresponds to the extension's `configure` method and is 
        responsible for early configuration, like adding PHP extension
        to the list of extensions the build pack will install.

        See build pack's extension documentation for the `configure`
        method.
        """
        pass

    def preprocess_commands(self):
        """Return list of preprocess commands to run once.

        This method maps to the extension's `preprocess_commands` method.
        """
        return ()

    def service_commands(self):
        """Return dictionary of service commands to run and keep running.

        This method maps to the extension's `service_commands` method.
        """
        return {}

    def service_environment(self):
        """Return dictionary of environment for the service commands.

        This method maps to the extension's `service_environment` method.
        """
        return {}

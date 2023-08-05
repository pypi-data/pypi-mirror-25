"""dtool_irods package."""

import sys
import logging
from subprocess import Popen, PIPE

__version__ = "0.3.1"

logger = logging.getLogger(__name__)


class CommandWrapper(object):
    """Class for creating API calls from command line tools."""

    def __init__(self, args):
        self.args = args

    def success(self):
        """Return True if the command line tool was run successfully."""
        return self.returncode == 0

# Useful helper functions

    def _call_cmd_line(self):
        """Run the command line tool."""
        try:
            logging.info("Calling Popen with: {}".format(self.args))
            p = Popen(self.args, stdout=PIPE, stderr=PIPE)
        except OSError:
            raise(RuntimeError("No such command found in PATH"))

        self.stdout, self.stderr = p.communicate()
        self.stdout = self.stdout.decode("utf-8")
        self.stderr = self.stderr.decode("utf-8")
        self.returncode = p.returncode

# Interface API.

    def __call__(self, exit_on_failure=True):
        """Return wrapped stdout or raise if stderr is not empty."""
        self._call_cmd_line()
        if self.success():
            return self.stdout
        else:
            if exit_on_failure:
                logger.warning("Command failed: {}".format(self.args))
                logger.warning(self.stderr)
                sys.stderr.write(self.stderr)
                sys.exit(self.returncode)
            else:
                logger.info("Command failed: {}".format(self.args))
                logger.info(self.stderr)

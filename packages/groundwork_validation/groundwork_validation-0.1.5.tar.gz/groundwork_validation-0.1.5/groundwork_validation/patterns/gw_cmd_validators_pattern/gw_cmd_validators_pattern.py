import sys
from re import finditer

from groundwork_validation.patterns import GwValidatorsPattern

# This uses a backport of subrprocess for python < 3
# This is needed to use the timeout functionality.
if sys.version_info[0] < 3:
    import subprocess32 as subprocess
else:
    import subprocess


class GwCmdValidatorsPattern(GwValidatorsPattern):
    """
    Allows the validation of output, return code and execution time of a given command.

    Usage::

        class My_Plugin(GwCmdValidatorsPattern):
            def __init__(self, app, **kwargs):
                self.name = "My_Plugin"
                super(My_Plugin, self).__init__(app, **kwargs)

            def activate(self):
                if self.validators.cmd.validate("dir", search="my_folder"):
                    print("Command 'dir' works a expected.")
                else:
                    print("Command 'dir' seems not to work correctly. We stop here")
                    sys.exit(1)

            def deactivate(self):
                pass
    """

    def __init__(self, app, **kwargs):
        super(GwCmdValidatorsPattern, self).__init__(app, **kwargs)
        self.app = app
        self.validators.cmd = CmdValidatorsPlugin(self)


class CmdValidatorsPlugin:

    def __init__(self, plugin):
        self.plugin = plugin

    def validate(self, command, search=None, regex=None, timeout=2, allowed_return_codes=None, decode="utf-8"):
        """
        Validates the output of a given command.

        The validation can be based on a simple string search or on a complex regular expression.
        Also the return_code can be validated. As well as the execution duration by setting a timeout.

        :param command: string, which is used as command for a new subprocess. E.g. 'git -v'.
        :param search: string, which shall be contained in the output of the command. Default is None
        :param regex:  regular expression, which is tested against the command output.
                       Default is None
        :param timeout: Time ins seconds, after which the execution is stopped and the validation fails.
                        Default is 2 seconds
        :param allowed_return_codes: List of allowed return values. Default is []
        :param decode: Format of the console encoding, which shall be used. Default is 'utf-8'
        :return: True, if validation succeeded. Else False.
        """
        if search is None and regex is None:
            raise ValueError("Parameter search or regex must be set.")
        if search is not None and regex is not None:
            raise ValueError("Only search OR regex is allowed to be used. Not both!")

        if allowed_return_codes is None:
            allowed_return_codes = []
        if isinstance(allowed_return_codes, int):
            allowed_return_codes = [allowed_return_codes]
        if not isinstance(allowed_return_codes, list):
            raise TypeError("allowed_return_code must be a list of integers")

        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, timeout=timeout)
            return_code = 0
        except subprocess.CalledProcessError as e:
            output = e.output
            return_code = e.returncode
        except subprocess.TimeoutExpired as e:
            raise CommandTimeoutExpired(e)

        if len(allowed_return_codes) > 0 and return_code not in allowed_return_codes:
            raise NotAllowedReturnCode("For command %s got return code '%s', which is not in %s"
                                       % (command, return_code, allowed_return_codes))

        self.plugin.log.debug("Executed '%s' with return code: %s" % (command, return_code))

        output = output.decode(decode)
        found = False
        if search is not None:
            if search in output:
                found = True
        elif regex is not None:
            for m in finditer(regex, output):
                self.plugin.log.debug("Found cmd validation '%s' at %02d-%02d" % (m.group(0), m.start(), m.end()))
                found = True
        return found


class NotAllowedReturnCode(BaseException):
    pass


class CommandTimeoutExpired(BaseException):
    pass

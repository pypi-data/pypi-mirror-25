import os
import subprocess
import re


class IPMIError(Exception):
    pass


class FreeIPMI(object):
    def __init__(self, sensors_cli_path=None):
        """Initialize an instance of the FreeIPMI class

        Args:
            sensors_cli_path (str): Path to the ipmi-sensors executable

        """

        if sensors_cli_path:
            self.sensors_cli_path = sensors_cli_path

            if not os.path.exists(sensors_cli_path):
                raise RuntimeError('{0} not found'.format(sensors_cli_path))

        else:
            self.sensors_cli_path = 'ipmi-sensors'

    def _execute(self, cmd):
        """Execute an IPMI command

        Args:
            cmd (str): Command to run

        Returns:
            str: The output of the command executed

        Raises:
            IPMIError

        """

        proc = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        if isinstance(out, bytes):
            out = out.decode()
        if isinstance(err, bytes):
            err = err.decode()

        if proc.returncode:
            ex = IPMIError(err.rstrip())
            ex.exitcode = proc.returncode
            raise ex
        else:
            return out

    def sensors(self):
        """Get all available IPMI sensors

        Returns:
            list: IPMI sensors

        """

        header = None
        sensors = []

        raw = self._execute(
            cmd="{} -Q --output-sensor-state --sdr-cache-recreate".format(self.sensors_cli_path))
        for row in [re.sub('\s+\|\s+', '|', line).split('|') for line in filter(None, raw.rstrip().split("\n"))]:
            if header:
                sensor = {}
                for index, value in enumerate(row):
                    # try figuring out the value type
                    v = None

                    try:
                        v = int(value)
                    except ValueError:
                        try:
                            v = float(value)
                        except ValueError:
                            v = re.sub("['\"]$", '', re.sub(
                                "^['\"]", '', value))

                            # convert N/A to None
                            if v.lower() == 'n/a':
                                v = None

                    sensor[header[index]] = v
                sensors.append(sensor)
            else:
                # the first line is the header
                header = [col.lower() for col in row]

        return sensors

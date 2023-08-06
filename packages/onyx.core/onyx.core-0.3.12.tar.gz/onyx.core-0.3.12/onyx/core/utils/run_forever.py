###############################################################################
#
#   Copyright: (c) 2017 Carlo Sbraccia
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
###############################################################################

import sys
import subprocess
import logging
import argh

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)-15s %(levelname)-8s %(name)-32s %(message)s"
)
logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
def run_forever(executable=None, script=None, logfile=sys.stdout):
    executable = executable or sys.executable

    if script is None:
        args = [executable]
    else:
        args = [executable, script]

    if sys.platform == "win32":
        # Don't display the Windows GPF dialog if the invoked program dies.
        # See comp.os.ms-windows.programmer.win32
        #  How to suppress crash notification dialog?, Jan 14,2004 -
	 #     Raymond Chen's response [1]   
        import ctypes
        SEM_NOGPFAULTERRORBOX = 0x0002 # From MSDN
        ctypes.windll.kernel32.SetErrorMode(SEM_NOGPFAULTERRORBOX);
        subprocess_flags = 0x8000000
    else:
        subprocess_flags = 0

    while True:
        try:
            with open(logfile, "a") as fout:
                subprocess.check_call(args, shell=False,
                                      stdout=fout, stderr=fout,
                                      creationflags=subprocess_flags)
        except subprocess.CalledProcessError as err:
            logger.error("subprocess died with error: {0!s}".format(err))


# -----------------------------------------------------------------------------
def main():
    argh.dispatch_command(run_forever)
        
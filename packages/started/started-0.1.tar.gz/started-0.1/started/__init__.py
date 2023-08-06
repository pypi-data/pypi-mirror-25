import contextlib
import shlex
import signal
import sys
from subprocess import Popen

def start(cmdline):
    return Popen(shlex.split(cmdline), stdout=sys.stdout, stderr=sys.stderr)


def stop(process):
    process.send_signal(signal.SIGINT)
    process.wait()


@contextlib.contextmanager
def started(cmdline):
    process = start(cmdline)
    try:
        yield process
    finally:
        stop(process)

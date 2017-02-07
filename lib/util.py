import os, sys, re, json
import platform
import shutil
from collections import defaultdict
from datetime import datetime
from decimal import Decimal
import traceback
import urlparse
import urllib
import threading

base_units = {'BTC':8, 'mBTC':5, 'uBTC':2}
fee_levels = [_('Within 25 blocks'), _('Within 10 blocks'), _('Within 5 blocks'), _('Within 2 blocks'), _('In the next block')]

class PrintError(object):
    '''A handy base class'''
    def diagnostic_name(self):
        return self.__class__.__name__

    def print_error(self, *msg):
        print_error("[%s]" % self.diagnostic_name(), *msg)

    def print_msg(self, *msg):
        print_msg("[%s]" % self.diagnostic_name(), *msg)

is_verbose = False

def print_error(*args):
    if not is_verbose: return
    print_stderr(*args)

def print_stderr(*args):
    args = [str(item) for item in args]
    sys.stderr.write(" ".join(args) + "\n")
    sys.stderr.flush()

def print_msg(*args):
    # Stringify args
    args = [str(item) for item in args]
    sys.stdout.write(" ".join(args) + "\n")
    sys.stdout.flush()
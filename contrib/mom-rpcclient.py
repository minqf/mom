#!/usr/bin/env python
# Memory Overcommitment Manager
# Copyright (C) 2011 Adam Litke, IBM Corporation
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

import xmlrpclib
from optparse import *
import sys

default_port = 8989

def ping(mom):
    if mom.ping():
        print "OK"

def usage(parser):
    parser.usageExit()

def main():
    global default_port
    usage = "usage: %prog [options] <command> [command_options]"
    parser = OptionParser(usage)
    parser.add_option('-p', '--port', dest='port', type='int',
                      default=default_port, metavar='PORT',
                      help='Connect using specified port number [%default]')
    cmds = OptionGroup(parser, "Commands",
                       "Select one of these commands to execute")
    cmds.add_option('--ping', dest='cmd', action='append_const', const='ping',
                    help='(No arguments) Ping the MOM RPC Server')
    parser.add_option_group(cmds)
    (options, args) = parser.parse_args()

    if options.cmd is None or len(options.cmd) != 1:
        parser.error("Exactly one command argument is required")

    mom = xmlrpclib.ServerProxy('http://localhost:%i' % options.port)
    try:
        if options.cmd[0] == 'ping':
            ping(mom)
    except Exception, e:
        print "Command '%s' failed: %s" % (options.cmd[0], e)
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
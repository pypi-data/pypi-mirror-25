#-------------------------------------------------------------------------
# run_ipgen.py
#
# IPgen: IP-core package generator for AXI4/Avalon
#
# Copyright (C) 2013, Shinya Takamaeda-Yamazaki
# License: Apache 2.0
#-------------------------------------------------------------------------
from __future__ import absolute_import
from __future__ import print_function
import os
import sys
import glob
if sys.version_info[0] < 3:
    import ConfigParser as configparser
else:
    import configparser

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import ipgen.utils.version
from ipgen.ipgen import SystemBuilder


#-------------------------------------------------------------------------
def main():
    from optparse import OptionParser
    INFO = "IPgen: IP-core package generator for AXI4/Avalon"
    VERSION = ipgen.utils.version.VERSION
    USAGE = "Usage: python run_ipgen.py [config] [-t topmodule] [-I includepath]+ [--memimg=filename] [--usertest=filename] [file]+"

    def showVersion():
        print(INFO)
        print(VERSION)
        print(USAGE)
        sys.exit()

    optparser = OptionParser()
    optparser.add_option("-v", "--version", action="store_true", dest="showversion",
                         default=False, help="Show the version")
    optparser.add_option("-t", "--top", dest="topmodule",
                         default="TOP", help="Top module of user logic, Default=userlogic")
    optparser.add_option("-I", "--include", dest="include", action="append",
                         default=[], help="Include path")
    optparser.add_option("-D", dest="define", action="append",
                         default=[], help="Macro Definition")
    optparser.add_option("--memimg", dest="memimg",
                         default=None, help="Memory image file, Default=None")
    optparser.add_option("--usertest", dest="usertest",
                         default=None, help="User-defined test code file, Default=None")
    optparser.add_option("--skip", action="store_true", dest="skip_not_found",
                         default=False, help="Skip not found modules")
    optparser.add_option("--ignore_protocol_error", action="store_true",
                         dest="ignore_protocol_error",
                         default=False, help="Ignore protocol error")
    optparser.add_option("--silent", action="store_true", dest="silent",
                         default=False, help="Silent mode")
    (options, args) = optparser.parse_args()

    filelist = []
    for arg in args:
        filelist.extend(glob.glob(os.path.expanduser(arg)))

    if options.showversion:
        showVersion()

    for f in filelist:
        if not os.path.exists(f):
            raise IOError("file not found: " + f)

    if len(filelist) == 0:
        showVersion()

    configfile = None
    userlogic_filelist = []
    for f in filelist:
        if f.endswith('.v'):
            userlogic_filelist.append(f)
        if f.endswith('.config'):
            if configfile is not None:
                raise IOError("Multiple configuration files")
            configfile = f

    if not options.silent:
        print("[Input Files]")
        print("  configuration: %s" % configfile)
        print("  user-logic: %s" % ', '.join(userlogic_filelist))

    # default values
    configs = {
        'single_clock': True,
        'if_type': 'axi',
        'output': 'out.v',
        'sim_addrwidth': 27,
        'hperiod_ulogic': 5,
        'hperiod_bus': 5,
    }

    confp = configparser.SafeConfigParser()
    if configfile is not None:
        confp.read(configfile)

    if confp.has_section('synthesis'):
        for k, v in confp.items('synthesis'):
            if k == 'single_clock':
                configs[k] = False if 'n' in v or 'N' in v else True
            elif k == 'signal_width' or k == 'ext_addrwidth' or k == 'ext_datawidth':
                configs[k] = int(v)
            elif k not in configs:
                raise ValueError("No such configuration item: %s" % k)
            else:
                configs[k] = v

    if confp.has_section('simulation'):
        for k, v in confp.items('simulation'):
            if k == 'sim_addrwidth' or k == 'hperiod_ulogic' or k == 'hperiod_bus':
                configs[k] = int(v)
            elif k not in configs:
                raise ValueError("No such configuration item: %s" % k)
            else:
                configs[k] = v

    if configs['hperiod_ulogic'] != configs['hperiod_bus']:
        raise ValueError(("Half period values of User-logic and Bus"
                          " should be same in current implementation"))

    builder = SystemBuilder()
    builder.build(configs,
                  options.topmodule,
                  userlogic_filelist,
                  include=options.include,
                  define=options.define,
                  usertest=options.usertest,
                  memimg=options.memimg,
                  skip_not_found=options.skip_not_found,
                  ignore_protocol_error=options.ignore_protocol_error,
                  silent=options.silent)

#-------------------------------------------------------------------------
if __name__ == '__main__':
    main()

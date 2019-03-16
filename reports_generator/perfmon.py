import os
import glob
from run_suite import utils
from run_suite.properties import Properties

def generate_charts():
    path = "%s/perfmon_*.jtl" % Properties.PERFMON_REPORT_DIR
    for filename in glob.glob(path):
        f = (os.path.splitext(os.path.basename(filename))[0])
        command = "JMeterPluginsCMD.sh --generate-png %s " +\
                  "--input-jtl %s --plugin-type PerfMon"
        command = command %\
            ("%s/%s_img.png" % (Properties.PERFMON_REPORT_DIR, f), filename)
        utils.run_command(command)
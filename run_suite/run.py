import utils
import parsers
from properties import Properties
from reports_generator import perfmon
from reports_generator import linechart
from reports_generator import custom_report


""" Form JMeter command based on the provided configs """
def get_jmeter_command(jmx, test_configs):
    jmeter_command = "jmeter.sh -n -t %s -l %s -e -o %s " +\
                     "-Jjmeter.save.saveservice.output_format=csv " +\
                     "-Jjmeter.save.saveservice.response_data=true " +\
                     "-Jjmeter.save.saveservice.samplerData=true " +\
                     "-Jjmeter.save.saveservice.requestHeaders=true " +\
                     "-Jjmeter.save.saveservice.url=true " +\
                     "-Jjmeter.save.saveservice.responseHeaders=true"
    jmeter_command = jmeter_command % (jmx,
                                       Properties.REPORT_FILE,
                                       Properties.REPORT_DIR)

    if test_configs.options:
        for key in test_configs.options:
            if key.upper() != 'GRANULARITY':
                jmeter_command += " -J%s=%s" %\
                                  (key.upper(), test_configs.options[key])
    jmeter_command += " -JREPORT_DIR %s" % Properties.PERFMON_REPORT_DIR
    return jmeter_command


def generate_reports(run_id, test_configs):
    """ Get granularity to calculate average values for tps and latency """
    utils.set_granularity(test_configs)

    """ Generate Latency vs TPS curve """
    linechart.generate_tps_vs_latency()

    """ Generate PerfMon reports as png images """
    perfmon.generate_charts()

    """ Generate custom report """
    custom_report.generate_report(run_id, test_configs)


def run_tests(jmx, config_file, report_dir, soft_cleanup, hard_cleanup):
    """ Parse provided config file """
    test_configs = parsers.TestConfigs(config_file)
    if not test_configs.is_test_config_provided():
        print("No configurations are provided. File is empty: " + config_file)
        exit(-1)

    """ Parse configs in each section and generate commands to run """
    for run_id in test_configs.get_sections():
        Properties.initialize(report_dir)

        """ Get and execute JMeter command """
        test_configs.set_options(run_id)
        jmeter_command = get_jmeter_command(jmx, test_configs)
        utils.run_command(jmeter_command)

        """ Generate reports """
        generate_reports(run_id, test_configs)

        """ Cleanup """
        utils.cleanup(soft_cleanup, hard_cleanup)
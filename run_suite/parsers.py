import os
import argparse
import ConfigParser


def parse_cmd_arguments():
    arguments = {}
    """ Define command line options """
    parser = argparse.ArgumentParser(description =\
        "Python script for doing Database Testing by running JMeter scripts \
        and generating reports in form of graphs.")
    parser.add_argument("-j", "--jmx", help="jmeter test plan")
    parser.add_argument("-c", "--config_file", help = "config file")
    parser.add_argument("-r", "--report_dir", default="../",
                        help = "generated reports directory")
    parser.add_argument("-sc", "--soft_cleanup", default="true",
                        help = "soft cleanup: remove only temporary files")
    parser.add_argument("-hc", "--hard_cleanup", default="false",
                        help = "hard cleanup: remove generated report files")

    """ Get command line arguments """
    args = parser.parse_args()
    arguments['jmx'] = args.jmx
    arguments['config_file'] = args.config_file
    arguments['report_dir'] = args.report_dir
    arguments['soft_cleanup'] = args.soft_cleanup
    arguments['hard_cleanup'] = args.hard_cleanup

    """ Report if some options are missing """
    if 'jmx' not in arguments or not arguments['jmx']:
        print("JMeter test plan is not provided.")
        exit(-1)

    if 'config_file' not in arguments or not arguments['config_file']:
        print("Config file is not provided.")
        exit(-1)

    """ Report if some options have invalid value """
    if not os.path.isfile(arguments['config_file']):
        print("File does not exist: " + arguments['config_file'])
        exit(-1)

    if arguments['soft_cleanup'].lower() not in ["false", "true"]:
        print("Invalid value for \"soft_cleanup\" option is specified: " +\
              arguments['soft_cleanup'])
        exit(-1)

    if arguments['hard_cleanup'].lower() not in ["false", "true"]:
        print("Invalid value for \"hard_cleanup\" option is specified: " +\
              arguments['hard_cleanup'])
        exit(-1)

    return arguments


""" Class for run configs """
class TestConfigs():
    def __init__(self, config_file):
        """ Read config file """
        self.config = ConfigParser.ConfigParser()
        self.config.read(config_file)
        self.options = {}

    def set_options(self, run_id):
        for option in self.config.options(run_id):
            value = self.config.get(run_id, option)
            self.options.update({option:value})

    def is_test_config_provided(self):
        return self.config.sections()

    def get_sections(self):
        return self.config.sections()
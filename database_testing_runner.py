from run_suite import run
from run_suite import parsers


""" Run database tests """
def main():
    arguments = parsers.parse_cmd_arguments()

    """ Temporary files are removed in case of soft cleanup.
        All generated report files are removed while using hard cleanup. """
    run.run_tests(arguments['jmx'],
                  arguments['config_file'],
                  arguments['report_dir'],
                  arguments['soft_cleanup'].lower(),
                  arguments['hard_cleanup'].lower())


if "__main__" == __name__:
    main()
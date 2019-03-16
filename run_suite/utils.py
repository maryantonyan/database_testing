import os
import shutil
import datetime
from properties import Properties
from subprocess import Popen, PIPE


def run_command(command):
    print("Running:\n%s\n\n" % command)
    process = Popen(['/bin/sh', '-l', '-c', command],
                     stdout = PIPE, stderr = PIPE)
    stdout, stderr = process.communicate()
    print(stdout)
    print(stderr)


def set_granularity(test_configs):
    if "granularity" in test_configs.options:
        Properties.GRANULARITY = int(test_configs.options["granularity"])
    else:
        Properties.GRANULARITY = 60


""" Remove generated temporary files """
def soft_cleanup():
    if os.path.exists("%s/temp/" % Properties.BASE_DIR):
        shutil.rmtree("%s/temp/" % Properties.BASE_DIR)
    run_command("pyclean .")


""" Remove generated reports """
def hard_cleanup():
    if os.path.exists(Properties.BASE_DIR):
        shutil.rmtree(Properties.BASE_DIR)


def cleanup(soft_cleanup, hard_cleanup):
    """ Cleanup """
    if soft_cleanup == "true":
        soft_cleanup()

    if hard_cleanup == "true":
        hard_cleanup()

    run_command("pyclean .")
import os
import datetime


class Properties():
    GENERATED_REPORTS_DIR = ""
    BASE_DIR = ""

    PROJECT_DIR = os.path.abspath("./reports_generator/LineGraph/LineGraph")
    APP_NAME = "com.instigatemobile.linegraph.ZoomableLineGraph"

    REPORT_IMG_PATH = ""
    REPORT_FILE = ""
    REPORT_DIR = ""
    PERFMON_REPORT_DIR = ""

    LATENCY_TMP_FILE = ""
    TPS_TMP_FILE = ""
    TMP_REPORT_FILE = ""
    JS_FILE_PATH = ""

    TPS_INFO_START = "var transactionsPerSecondInfos ="
    TPS_INFO_END = "// Transactions per second"
    LATENCY_INFO_START = "var latenciesOverTimeInfos ="
    LATENCY_INFO_END = "// Latencies Over Time"
    LATENCY_LABEL = ""

    GRANULARITY = 0

    @staticmethod
    def initialize(report_dir):
        now = datetime.datetime.now()
        Properties.GENERATED_REPORTS_DIR = os.path.abspath(report_dir)
        Properties.BASE_DIR = os.path.abspath("./reports/%s") % now.strftime("%Y_%m_%d_%H_%M")

        Properties.REPORT_IMG_PATH = "%s/report_img.png" % Properties.BASE_DIR
        Properties.REPORT_FILE = "%s/generated_report.csv" % Properties.BASE_DIR
        Properties.REPORT_DIR = "%s/dashboard_report" % Properties.BASE_DIR
        Properties.PERFMON_REPORT_DIR = "%s/perfmon_report" % Properties.BASE_DIR

        Properties.LATENCY_TMP_FILE = "%s/temp/tmp_latency_file.json" % Properties.BASE_DIR
        Properties.TPS_TMP_FILE = "%s/temp/tmp_tps_file.json" % Properties.BASE_DIR
        Properties.TMP_REPORT_FILE = "%s/temp/tmp_report.csv" % Properties.BASE_DIR

        Properties.JS_FILE_PATH = "%s/content/js/graph.js" % Properties.REPORT_DIR

        if not os.path.exists(Properties.BASE_DIR):
            os.makedirs(Properties.BASE_DIR)

        if not os.path.exists("%s/temp" % Properties.BASE_DIR):
            os.makedirs("%s/temp" % Properties.BASE_DIR)
import os
import glob
import shutil
from os.path import basename
from run_suite.properties import Properties


def generate_content(title, path, testbox_ip, teradata_ip):
    content = ""
    files = glob.glob("%s/*.png" % path)
    if (len(files) != 0):
        content += "<h1>%s</h1>" % title
        for f in files:
            filename = basename(f)
            content += "<div class=\"image\">"
            if "perfmon" in filename:
                start = filename.find("_")
                end = filename.rfind("_")
                chart_name = filename[start : end]
                subtitle = chart_name.replace("_", " ").upper()
                content += "<h3>%s</h3>" % subtitle
                content += "<p>%s - TestBox</p>" % testbox_ip
                content += "<p>%s  - Teradata</p>" % teradata_ip
                image = "perfmon_report/%s" % os.path.basename(f)
            else:
                image = os.path.basename(f)
            content += "<a href='%s'><img src='%s'></a></div>" % (image, image)
    return content


def replace_in_file(file_path, text_to_search, replacement_text):
    file_content = open(file_path).read()
    file_content = file_content.replace(text_to_search, replacement_text)
    with open(file_path, 'w') as f:
        f.write(file_content)


def generate_index_php(report_dir, testbox_ip, teradata_ip):
    php_path = "%s/index.php" % report_dir

    curve_info = generate_content("Latency / TPS curve", report_dir, testbox_ip, teradata_ip)
    replace_in_file(php_path, "LATENCY_VS_TPS_CURVE", curve_info)

    perfmon_info = generate_content("PerfMon Metrics Reports", "%s/perfmon_report" % report_dir, testbox_ip, teradata_ip)
    replace_in_file(php_path, "PERFMON_REPORTS", perfmon_info)


def generate_report(run_id, test_configs):
    """ Get Test ID """
    test_id = run_id[4:]

    """ Generate reports folder """
    report_dir = "%s/%s" % (Properties.GENERATED_REPORTS_DIR, test_id)
    if os.path.exists(report_dir):
        shutil.rmtree(report_dir)
    os.makedirs(report_dir)

    """ Copy index.php into report directory """
    shutil.copy("./templates/index.php", report_dir)
    shutil.copy("./templates/resources/img/logo.svg", report_dir)

    """ Copy latency / tps curve report images """
    shutil.copy("%s/report_img.png" % Properties.BASE_DIR, report_dir)

    """ Copy JMeter dashboard report to web server """
    dashboard_report_dir = "%s/dashboard_report" % report_dir
    shutil.copytree(Properties.REPORT_DIR, dashboard_report_dir)

    """ Copy PerfMon reports to web server """
    perfmon_report_dir = "%s/perfmon_report" % report_dir
    os.makedirs(perfmon_report_dir)
    for pngfile in glob.iglob("%s/*.png" % Properties.PERFMON_REPORT_DIR):
        shutil.copy(pngfile, perfmon_report_dir)

    generate_index_php(report_dir, test_configs.options['testbox_ip'], test_configs.options['teradata_ip'])
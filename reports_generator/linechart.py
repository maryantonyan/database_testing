import json
from run_suite import utils
from operator import itemgetter
from run_suite.properties import Properties


def retrieve_data(info_start, info_end, tmp_file_path):
    """ Retrieve info from js file """
    content = open(Properties.JS_FILE_PATH).read()
    start = content.index(info_start)
    end = content.index(info_end)
    content = content[start:end]

    """ Retrieve data """
    start = content.index("\"series\":")
    end = content.index("}],")
    content = "{" + content[start:end] + "}]}"

    """ Write json data into file """
    open(tmp_file_path, 'w+').write(content)


""" Load json file into dictionary """
def load_data_into_dict(tmp_file_path):
    data = None
    with open(tmp_file_path) as f:
        data = json.load(f)
    return data


""" Sort retrieved data by elapsed time """
def sort(item):
    """ Extract statement execution status """
    data = item["data"]
    label = item["label"].split('-')

    """ Get label for tps"""
    label = label[-1]

    """ Set label for latency """
    if label not in ["success", "failure"]:
        label = "statement"
        Properties.LATENCY_LABEL = label

    list_of_tuples = [tuple(l) for l in data]
    list_of_tuples = sorted(list_of_tuples, key=itemgetter(0))

    return (label, list_of_tuples)


def sort_by_elapsed_time(data):
    retrieved_values = {}
    """ Sort retrieved data by elapsed time """
    for item in data:
        label, values = sort(item)
        if label not in retrieved_values:
            retrieved_values[label] = []
        retrieved_values[label] += values
    return retrieved_values


def chunks(data, GRANULARITY = 60):
    return (data[x : x + GRANULARITY] for x in range(0, len(data), GRANULARITY))


def get_average(array):
    return (sum([pair[0] for pair in array]) / len(array), sum([pair[1] for pair in array]) / len(array))


def get_average_data(data):
    """ Slice data and get averages """
    averages = []
    for item in chunks(data, Properties.GRANULARITY):
        averages.append(get_average(item))
    return averages


def to_dict(list_of_tuples):
    dictionary = {}
    for item in list_of_tuples:
        dictionary["%s" % hash(round(item[0], 1))] = item[1]
    return dictionary


def prepare_data_for_chart(tps_values, latency_values):
    prepared_data = {}
    latency_dict = to_dict(latency_values)
    for label in tps_values:
        tps_dict = to_dict(tps_values[label])
        prepared_data[label] = []
        for elapsed_time in tps_dict:
            prepared_data[label].append((tps_dict[elapsed_time], latency_dict[elapsed_time]))
    return prepared_data


""" Write tps and latency in csv  file """
def write_into_file(data, label):
    with open(Properties.TMP_REPORT_FILE, 'a+') as f:
        for i in range(0, len(data)):
            f.write("%s,%s,%s\n" % (data[i][0], data[i][1], label))


""" Generate csv file with tps and latency in it """
def generate_csv_file():
    """ Get latency and tps values from reports generated by JMeter """
    retrieve_data(Properties.TPS_INFO_START, Properties.TPS_INFO_END, Properties.TPS_TMP_FILE)
    retrieve_data(Properties.LATENCY_INFO_START, Properties.LATENCY_INFO_END,
                  Properties.LATENCY_TMP_FILE)

    """ Load tps and latency data into dictionaries """
    tps_data = load_data_into_dict(Properties.TPS_TMP_FILE)
    latency_data = load_data_into_dict(Properties.LATENCY_TMP_FILE)

    """ Sort retrieved data by elapsed time """
    tps_values = sort_by_elapsed_time(tps_data["series"])
    latency_values = sort_by_elapsed_time(latency_data["series"])

    """ Extract latencies without label """
    latency_values = latency_values[Properties.LATENCY_LABEL]

    """ Get data for chart generation """
    prepared_data = prepare_data_for_chart(tps_values, latency_values)

    """ Generate CSV file """
    with open(Properties.TMP_REPORT_FILE, 'w+') as f:
        f.write("%s,%s,%s\n" % ("tps", "latency", "label"))
    for label in prepared_data:
        averages = get_average_data(prepared_data[label])

        """ Append to CSV file """
        write_into_file(averages, label)


def generate_tps_vs_latency():
    """ Generate csv file needed for generation of graph report """
    generate_csv_file()

    """ Run Java application to generate graph report """
    java_command = "cd %s;mvn compile;" % (Properties.PROJECT_DIR) +\
                   "mvn exec:java -Dexec.mainClass=%s " % Properties.APP_NAME +\
                   "-Dexec.args=\"%s %s %s\"" % (Properties.TMP_REPORT_FILE,
                                                 Properties.REPORT_IMG_PATH,
                                                 Properties.GRANULARITY)
    utils.run_command(java_command)
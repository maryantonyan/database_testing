This is the README file for the database testing tool.

-------------------------------------------------------------------------------
CONTENTS
-------------------------------------------------------------------------------

  - Author
  - Introduction
  - Directory Structure
  - Before you begin
  - Usage
  - Config File Example


-------------------------------------------------------------------------------
AUTHOR
-------------------------------------------------------------------------------
Meri Antonyan

E-mail: meri_a@instigatemobile.com

Tel: +374-98-745113


-------------------------------------------------------------------------------
INTRODUCTION
-------------------------------------------------------------------------------

This project is defined for running database testing and providing the results.


-------------------------------------------------------------------------------
DIRECTORY STRUCTURE
-------------------------------------------------------------------------------

```
├── README.md
├── database_testing_runner.py
├── jmeter_test_suite
│   ├── config.ini
│   ├── connect_to_db_performance_testing.jmx
│   └── input
│       ├── input.sql
│       ├── run_1.sql
│       ├── run_2.sql
│       ├── run_6.1.sql
│       ├── run_6.2.sql
│       └── run_8.sql
├── reports_generator
│   ├── __init__.py
│   ├── custom_report.py
│   ├── perfmon.py
│   ├── linechart.py
│   └── LineGraph
│       └── LineGraph
│           ├── css
│           │   └── style.css
│           ├── pom.xml
│           ├── src
│           │   └── main
│           │       └── java
│           │           └── com
│           │               └── instigatemobile
│           │                   └── linegraph
│           │                       └── ZoomableLineGraph.java
├── run_suite
│   ├── __init__.py
│   ├── parsers.py
│   ├── properties.py
│   ├── run.py
│   └── utils.py
└── templates
    ├── index.html
    └── resources
        └── img
            └── logo.svg
```


-------------------------------------------------------------------------------
BEFORE YOU BEGIN
-------------------------------------------------------------------------------
Before you begin you need to install:
  - Java / OpenJFX
  - JMeter / JMeter Plugins Manager
  - CMD Runner
  - JMeter Plugins:
    - Custom Thread Group plugin
    - Perfmon Metrics plugin
    - JDBC Support
    - Command-Line Graph Plotting Tool
  - JDBC Drivers
    - Teradata JDBC Driver
    - PostgeSQL JDBC Driver
  - Maven
if you don't have them already installed.

**Ubuntu**
To install ```Java``` type:
```
sudo apt install default-jre
sudo apt install default-jdk
```

To install ```OpenJFX``` package type:
```
sudo apt install openjfx
```

To install ```JMeter``` follow the instructions:
```
wget -c http://ftp.ps.pl/pub/apache//jmeter/binaries/apache-jmeter-5.1.zip
unzip apache-jmeter-5.1.zip
```
Add ```${INSTALL_DIR}/apache-jmeter-5.1/bin``` to ```PATH``` variable.


To install ```JMeter Plugin Manager``` follow the link:
```
wget --content-disposition http://search.maven.org/remotecontent?filepath=kg/apc/jmeter-plugins-manager/1.3/jmeter-plugins-manager-1.3.jar
```
and place it under ```${JMETER_HOME}/lib/ext``` directory.


To install ```CMD Runner``` type:
```
wget --content-disposition http://search.maven.org/remotecontent?filepath=kg/apc/cmdrunner/2.2/cmdrunner-2.2.jar
```
and place it under ```${JMETER_HOME}/lib``` directory.


Run the following command to have ```PluginsManagerCMD.sh``` file in
```${JMETER_HOME}/bin``` directory:
```
java -cp ./lib/ext/jmeter-plugins-manager-1.3.jar org.jmeterplugins.repository.PluginManagerCMDInstaller
```


Install needed plugins using ```JMeter Plugins Manager``` command line:
```
./bin/PluginsManagerCMD.sh install jpgc-perfmon
./bin/PluginsManagerCMD.sh install jpgc-casutg
./bin/PluginsManagerCMD.sh install jmeter-jdbc
./bin/PluginsManagerCMD.sh install jpgc-cmd
```


Download ```Teradata JDBC Driver``` from the link below and copy two jar files
```terajdbc4.jar``` and ```tdgssconfig.jar``` into JMeter's lib directory.
```
http://downloads.teradata.com/download/connectivity/jdbc-driver
```

Download ```PostgreSQL JDBC Driver``` and copy jar file into
```${JMETER_HOME}/lib``` directory.
```
wget --content-disposition https://jdbc.postgresql.org/download/postgresql-42.2.4.jar
```

To download and install ```Maven``` type:
```
sudo apt-get install maven
```

**Mac**
To install ```Java``` follow the steps described in the following link:
```
TODO
```

To install ```OpenJFX``` package follow the link:
```
TODO
```

To install ```JMeter``` with extra plugins follow the instructions:
```
brew install jmeter --with-plugins
```

Download ```Teradata JDBC Driver``` from the link below and copy two jar files
```terajdbc4.jar``` and ```tdgssconfig.jar``` into JMeter's lib directory.

```
http://downloads.teradata.com/download/connectivity/jdbc-driver
```

Download ```PostgreSQL JDBC Driver``` and copy jar file into
```${JMETER_HOME}/lib``` directory.

```
wget --content-disposition https://jdbc.postgresql.org/download/postgresql-42.2.4.jar
```

To download and install ```Maven``` follow the instructions:
```
http://www.baeldung.com/install-maven-on-windows-linux-mac
```


-------------------------------------------------------------------------------
USAGE
-------------------------------------------------------------------------------

Python script for doing Database Testing by running JMeter scripts and
generating reports in form of graphs.


usage:
```
python database_testing_runner.py [-h] [-j JMX] [-c CONFIG_FILE] [-r REPORT_DIR]
                                  [-sc SOFT_CLEANUP] [-hc HARD_CLEANUP]
```


command line arguments:
```
  -h, --help                                     show this help message and exit
  -j JMX, --jmx JMX                              JMeter test plan
  (required)
  -c CONFIG_FILE, --config_file CONFIG_FILE      config file
  (required)
  -r REPORT_DIR, --report_dir REPORT_DIR         generated reports directory
  (optional)                                     DEFAULT: ../
  -sc SOFT_CLEANUP, --soft_cleanup SOFT_CLEANUP  soft cleanup: true | false
                                                 remove only temporary files
  (optional)                                     DEFAULT: true
  -hc HARD_CLEANUP, --hard_cleanup HARD_CLEANUP  hard cleanup:
                                                 remove generated report files
  (optional)                                     DEFAULT: false
```


run example:
```
python database_testing_runner.py \
       --jmx jmeter_test_suite/connect_to_db_performance_testing.jmx \
       --config_file jmeter_test_suite/config.ini \
       --report_dir /var/www/html/database_testing/reports/test_plan \
       --soft_cleanup true
```


-------------------------------------------------------------------------------
CONFIG FILE EXAMPLE
-------------------------------------------------------------------------------

```
....

[run_1]
NUM_OF_USERS = 100
INITIAL_DELAY = 2
USERS_RAMP_UP = 10
RAMP_UP_STEP_COUNT = 10
FULL_LOAD_PERIOD = 5
USERS_STOP_PERIOD = 0
NUM_OF_CONNECTIONS = 0
CONNECTION_TIMEOUT = 10000
DATABASE_URL = jdbc:teradata://37.252.70.55/testing_db
JDBC_DRIVER_CLASS = com.teradata.jdbc.TeraDriver
TESTBOX_IP = localhost
TERADATA_IP = 37.252.70.55
USERNAME = dbc
PASSWORD = dbc
INPUT_FILE = ./input/run_1.sql
GRANULARITY = 10

....
```
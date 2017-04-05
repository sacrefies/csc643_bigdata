# Hadoop 2.7.x on Windows
Hadoop's official releases are not for `Windows` platform. If the target platform is `Windows`, it requires source checkout and building locally with third-party tool sets.

However, there are some built-ready packages which can be used directly for an installation on `Windows`.

## Installation
Follow the instructions below:
+ Download the package at the [Official Hadoop Releases][hadoop_releases] page.
+ Extract the downloaded package into the destination directory, for instance, `D:\hadoop`.
+ Download all the files from the `winutils` for `Hadoop 2.7.x` at [this `GitHub` repo][winutils].
+ Replace the files under `D:\hadoop\bin` with the ones from the `winutils`.

Now, this `non-Windows` release has become a `Windows` release.

## Running the Hadoop Services
This section shows the configuration and commands to run the `Hadoop` servers/services with one node for a development environment.

Please refer to [Hadoop on Windows][ref_setup] document for more details.

### Configuration

### Environment Variables
There are couple of environment variables which need to be set before any `Hadoop` services can run:
+ `JAVA_HOME`
+ `HADOOP_HOME`

These 2 variables must be set in the `system variables`. The below snippet shows an example, assuming the root directory of the installation is `D:\hadoop`.
```cmd
JAVA_HOME=D:\java\jdk1.8_48
HADOOP_HOME=D:\hadoop
```

### HDFS Configuration
`Hadoop` also uses a set of `XML` files to manage the global variables in its own domain.

There are a few mandatory files to create or modify beforehand to launch the services/servers. Please also refer to ["Starting a Single Node (pseudo-distributed) Cluster"][win_conf] for further details.

Assuming the root directory of the installation is `D:\hadoop`, and `HADOOP_HOME` is set as the root directory:

+ Edit the file `%HADOOP_HOME%\etc\hadoop\hadoop-env.cmd`: Add the following lines right after the line `set JAVA_HOME=%JAVA_HOME%`:
```cmd
set HADOOP_PREFIX=%HADOOP_HOME%
set HADOOP_CONF_DIR=%HADOOP_PREFIX%\etc\hadoop
set YARN_CONF_DIR=%HADOOP_CONF_DIR%
```

+ Create or edit the file `%HADOOP_HOME%\etc\hadoop\core-site.xml`:
```xml
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>
```

+ Create or edit the file `%HADOOP_HOME%\etc\hadoop\hdfs-site.xml`:
```xml
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
</configuration>
```

+ Edit or create the file `%HADOOP_HOME%\etc\hadoop\slaves` and make sure it has the following entry:  
```properties
localhost
```

The default configuration puts the `HDFS` metadata and data files under `\tmp` on the current drive.
In the above example this would be `D:\tmp`. For your first test setup you can just leave it at the default.

### YARN Configuration
+ Edit or create the file `%HADOOP_HOME%\etc\hadoop\mapred-site.xml` and add the following entries:
```xml
<configuration>

    <property>
        <name>mapreduce.job.user.name</name>
        <value>%USERNAME%</value>
    </property>

    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>

    <property>
        <name>yarn.apps.stagingDir</name>
        <value>/user/%USERNAME%/staging</value>
    </property>

    <property>
        <name>mapreduce.jobtracker.address</name>
        <value>local</value>
    </property>
</configuration>
```

+ Edit or create the file `%HADOOP_HOME%\etc\hadoop\yarn-site.xml` and add the following entries:
```xml
<configuration>

    <property>
        <name>yarn.server.resourcemanager.address</name>
        <value>0.0.0.0:8020</value>
    </property>

    <property>
        <name>yarn.server.resourcemanager.application.expiry.interval</name>
        <value>60000</value>
    </property>

    <property>
        <name>yarn.server.nodemanager.address</name>
        <value>0.0.0.0:45454</value>
    </property>

    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>

    <property>
        <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
        <value>org.apache.hadoop.mapred.ShuffleHandler</value>
    </property>

    <property>
        <name>yarn.server.nodemanager.remote-app-log-dir</name>
        <value>/app-logs</value>
    </property>

    <property>
        <name>yarn.nodemanager.log-dirs</name>
        <value>/dep/logs/userlogs</value>
    </property>

    <property>
        <name>yarn.server.mapreduce-appmanager.attempt-listener.bindAddress</name>
        <value>0.0.0.0</value>
    </property>

    <property>
        <name>yarn.server.mapreduce-appmanager.client-service.bindAddress</name>
        <value>0.0.0.0</value>
    </property>

    <property>
        <name>yarn.log-aggregation-enable</name>
        <value>true</value>
    </property>

    <property>
        <name>yarn.log-aggregation.retain-seconds</name>
        <value>-1</value>
    </property>

    <property>
        <name>yarn.application.classpath</name>
        <value>%HADOOP_CONF_DIR%,%HADOOP_COMMON_HOME%/share/hadoop/common/*,%HADOOP_COMMON_HOME%/share/hadoop/common/lib/*,%HADOOP_HDFS_HOME%/share/hadoop/hdfs/*,%HADOOP_HDFS_HOME%/share/hadoop/hdfs/lib/*,%HADOOP_MAPRED_HOME%/share/hadoop/mapreduce/*,%HADOOP_MAPRED_HOME%/share/hadoop/mapreduce/lib/*,%HADOOP_YARN_HOME%/share/hadoop/yarn/*,%HADOOP_YARN_HOME%/share/hadoop/yarn/lib/*</value>
    </property>

</configuration>
```

+ Finally, open `%HADOOP_HOME%\bin\yarn.cmd`, change the line endings to the `Windows` convention, `CRLF`.

### Launching the Daemons

#### Initialization
+ Run `%HADOOP_HOME%\etc\hadoop\hadoop-env.cmd` to setup environment variables that will be used by the startup scripts and the daemons.
+ Format the filesystem with the following command:
```cmd
> %HADOOP_HOME%\bin\hdfs namenode -format
```
This command will print a number of filesystem parameters. Just look for the following two strings to ensure that the format command succeeded.
```cmd
14/01/18 08:36:23 INFO namenode.FSImage: Saving image file \tmp\hadoop-username\dfs\name\current\fsimage.ckpt_0000000000000000000 using no compression
14/01/18 08:36:23 INFO namenode.FSImage: Image file \tmp\hadoop-username\dfs\name\current\fsimage.ckpt_0000000000000000000 of size 200 bytes saved in 0 seconds.
```

#### Launching the Daemons
+ To launch the `NameNode` and `DataNode` on `localhost`:
```cmd
> %HADOOP_HOME%\sbin\start-dfs.cmd
```
+ to launch `YARN`:
```cmd
%HADOOP_HOME%\sbin\start-yarn.cmd
```

<!-- References -->
[hadoop_releases]: http://hadoop.apache.org/releases.html "Apache Hadoop Releases"
[winutils]: https://github.com/steveloughran/winutils/tree/master/hadoop-2.7.1/bin/ "Windows Runnable"
[win_conf]: http://hadoop.apache.org/docs/r2.7.3/hadoop-project-dist/hadoop-common/SingleCluster.html#Pseudo-Distributed_Operation "Configurations for Windows"
[ref_setup]: https://wiki.apache.org/hadoop/Hadoop2OnWindows

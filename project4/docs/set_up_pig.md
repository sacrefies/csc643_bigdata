# PIG Installation
This document is a step-by-step guidance which is extracted from the official [PIG Getting Started][pig_getstarted] document.

## Prerequisites
Both [Hadoop 2.x][hadoop_releases] and `JDK7` or higher version of `Java` are mandatorily required.

## Installation
Follow the following steps:
1. Log into the VM `Happy` with a user who has the permission to run `sudo` command.
1. Download a recent stable release from one of the [releases][pig_releases].
1. Unpack the downloaded `PIG` distribution, and then note the following:
    + The unpacked `PIG` distribution can be put under any directory. However, it's recommended to put it where the `Hadoop 2.x` distribution resides.
1. Change the permissions of the files under the installation's `bin` sub-directory:
    ```bash
    $ sudo chmod +x /<my-path-to-pig>/bin/*.*
    ```
1. Log into the shell of the user `hduser`:
    ```bash
    $ su - hduser
    ```
1. In `hduser`'s `.bashrc`, add a new environment variable `$PIG_HOME` pointing to the root directory of the `PIG` installation path. For example:
    ```bash
    $ export PIG_HOME=/<my-path-to-pig>/pig-n.n.n
    ```
1. In `hduser`'s `.bashrc`, add `$PIG_HOME/bin` to `$PATH`. For example:
    ```bash
    $ export PATH=/<my-path-to-pig>/pig-n.n.n/bin:$PATH
    ```

# Running PIG
1. Test the `PIG` installation with this simple command:
    ```bash
    $ pig -help
    ```
    The help message should be correctly printed, as the following:
    ```bash
    Apache Pig version 0.16.0 (r1746530)
    compiled Jun 01 2016, 23:10:49

    USAGE: Pig [options] [-] : Run interactively in grunt shell.
           Pig [options] -e[xecute] cmd [cmd ...] : Run cmd(s).
           Pig [options] [-f[ile]] file : Run cmds found in file.
    ...

    17/04/17 15:25:22 INFO pig.Main: Pig script completed in 361 milliseconds (361 ms)
    ```
1. Enter the `grunt` interactive shell with this command:
    ```bash
    $ pig -x mapreduce
    ```
    Then the shell should be launched, as the following:
    ```bash
    17/04/17 15:29:25 INFO pig.ExecTypeProvider: Trying ExecType : LOCAL
    17/04/17 15:29:25 INFO pig.ExecTypeProvider: Trying ExecType : MAPREDUCE
    17/04/17 15:29:25 INFO pig.ExecTypeProvider: Picked MAPREDUCE as the ExecType
    ...

    grunt>
    ```


<!-- References -->
[hadoop_releases]: http://hadoop.apache.org/releases.html "Apache Hadoop Releases"
[pig_getstarted]: http://pig.apache.org/docs/r0.16.0/start.html#Pig+Setup "Getting Started"
[pig_releases]: http://hadoop.apache.org/pig/releases.html "PIG Releases"

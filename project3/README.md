# The Project
This project work with the [Housing Affordability Data System][apache_hadoop], which is a set of files derived from the 1985 and later national American Housing Survey (AHS) and the 2002 and later Metro AHS. The data is provided by [the U.S goverment's open data][gov_data].

This project is developed in `Java` with `JDK7` and is designed for [Apache Hadoop 2.7.x][apache_hadoop], to analyze [the 2013 HADS data][hads_2013] and compute the correlation between:
+ Occupant data
    + Age of the head of the house hold
    + Number of persons in the household
    + Owner/renter status
+ Location
    + City and Suburban
    + Region
+ Income
    + Household income

There can be many perspectives/angles to use/cook and to analyze the data. Here is *Team 1*'s [formula][multi_regression]

*See the [project report](docs/report.md) for details.*

## Working in A Windows Environment
If working in a Windows development environment and local testing is needed, a [Hadoop][apache_hadoop] system for the Windows platform should be installed.

Please see [Install and Configure Hadoop on Windows](docs/set_up_win_dev.md) document.

<!-- Reference links -->
[apache_hadoop]: http://hadoop.apache.org/  "Apache Hadoop Project Home"
[hadoop_docs]: http://hadoop.apache.org/docs/r2.7.3/  "Apache Hadoop 2.7.3 Documentation"
[hadoop_releases]: http://hadoop.apache.org/releases.html "Apache Hadoop Releases"
[hads]: https://www.huduser.gov/portal/datasets/hads/hads.html "American Housing Survey: Housing Affordability Data System"
[hads_docs]: https://www.huduser.gov/portal/datasets/hads/HADS_doc.pdf "HADS Documentation"
[gov_data]: https://www.data.gov/ "The Home of the U.S. Government's Open Data"
[hads_2013]: https://www.huduser.gov/portal/datasets/hads/hads2013n_ASCII.zip "HADS Data 2013"
[multi_regression]: "docs/multiple_regression_instruction.md" "Multiple Regression"

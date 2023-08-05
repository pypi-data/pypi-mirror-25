Navigator Optimizer Upload CLI option. this command is used to upload file to Navigator
Optimizer. The options section describes the parameters in more details. The uploaded
file can be either an .sql file which comprise of multiple queries or .csv file. The csv
file header is used to deduce different fields, slice and dice a feature within
Navigator Optimizer uses this information.

======================
Options
======================
* **--file-location** - The path of a query file on local file system, that needs to be uploaded, for e.g. /path/to/myfile.
* **--source-platform** - The platform where this queries in a file were executed, for e.g. oracle, teradata, impala, hive etc.
* **--col-delim** -  The column delimiter if any for this file, default is null string, applicable for csv style file, ignored for .sql file.
* **--row-delim** - The row delimiter if any for this file, default is null string, applicable for csv style file, ignored for .sql file.
* **--file-name** - Target file name, for the file location that was passed, if omitted file name will be derived from file location.
* **--header-fields** - The per column header information associated with csv style file. This is a list that describes detail for each column, as described below
  * **coltype** - Type of the column, its an enumn, type could be either of ["NONE", "SQL_ID", "SQL_QUERY", "ELAPSED_TIME"]
  * **use** - Indicates if specified field should be used for computation.
  * **count** - Count the specified field
  * **name** - The column name in csv file
  * **tag** - This is used to set custom column type
* **--tenant** - The tenant information corresponding to a user. This information could be retrieved via "cws navopt get-tenant --email <user email address>"

======================
Output
======================
* **status** - Information about status of upload.
               state - The status of a upload
               workloadId - The id of a workload. This id could be used to find current status via "altus navopt workload-info --tenant <value> --workloadId <value>"

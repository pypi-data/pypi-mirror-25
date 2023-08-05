**1. To submit Hive jobs to a cluster**

- Command::

    altus dataeng submit-jobs --cluster-name cluster-name --jobs name="My Hive Job 1",hiveJob='{script=file:///path/on/my/local/filesystem/to/jobOne.hql}' name="My Hive Job 2",hiveJob='{script=file:///path/on/my/local/filesystem/to/jobTwo.hql}'

- Optional parameters::

    name, failureAction

- Required parameters::

    hiveJob

- Required hiveJob fields::

    script

- Optional hiveJob fields::

    params, jobXml

**2. To submit Spark jobs to a cluster**

- Command::

    altus dataeng submit-jobs --cluster-name cluster-name --jobs name="My Spark Job 1",sparkJob='{jars=[s3a://path/to/jar1.jar, s3a://path/to/jar1.jar], mainClass=org.myorg.Main}' name="My Spark Job 2",sparkJob='{jars=[s3a://path/to/jar1.jar, s3a://path/to/jar1.jar], mainClass=org.myorg.Main}'

- Optional parameters::

    name, failureAction

- Required parameters::

    sparkJob

- Required sparkJob fields::

    jars

- Optional sparkJob fields::

    mainClass, applicationArguments, sparkArguments

**3. To submit MR2 jobs to a cluster**

- Command::

    altus dataeng submit-jobs --cluster-name cluster-name --jobs name="My MR2 Job 1",mr2Job='{mainClass=org.myorg.Main, jars=s3a://path/to/jar.jar}' name="My MR2 Job 2",mr2Job='{mainClass=org.myorg.Main, jars=s3a://path/to/jar.jar}'

- Optional parameters::

    name, failureAction

- Required parameters::

    mr2Job

- Required mr2Job fields::

    mainClass, jars

- Optional mr2Job fields::

    arguments, javaOpts, jobXml

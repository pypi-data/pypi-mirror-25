Suppose you want to upload .sql file::

    $ altus navopt --endpoint-url="http://localhost:443" upload --file-location "tpch.sql" --tenant "7e978efb-6c7e-0bef-d9fc-ada5e584977d" --file-name="tpch.sql" --source-platform "impala" --auth-config <key>.json
    {
      "status": {
        "state": "WAITING",
        "workloadId": "aba8983a-84d1-4b0b-9a84-f8f267804057"
      }
    }

Suppose you want to upload .csv file::

    $ altus --auth-config <key>.json --endpoint-url="http://localhost:443" navopt upload --tenant "7e978efb-6c7e-0bef-d9fc-ada5e584977d" --source-platform "impala" --file-name "file.csv" --row-delim "\n" --col-delim "," --header-fields count=0,coltype=NONE,use=true,tag='users',name=users count=0,coltype=SQL_QUERY,use=true,tag='',name=query
    {
      "status": {
        "state": "WAITING",
        "workloadId": "b3b9eef1-f7f1-46f7-9b41-577ccbab3eb8"
      }
    }

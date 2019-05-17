# Archive PB Job

### Program Type:

	Batch Job

### Execution Frequency:

	Weekly

### Program Description

This job creates weekly tar.gz archives from a directory of .pb files. Current week is excluded from this operation.

The program can be run independently from other services or dependent on the Data API Service to retrieve timezone and dataset name information.

### Program Execution (API Dependent)

```
docker run --rm --network=my_network -e "API_URL=http://basic_api" -e "DATASET=hart" -v /transi/data/pb/hart:/usr/src/app/pb -v /transi/data/tar/hart:/usr/src/app/tar registry.gitlab.com/cutr-at-usf/transi/core/archive-pb
```

### Execution Parameters

**API_URL**: URL used to access the Data API Service on docker network

**DATASET**: Dataset configuration name as specified in config.json for the Data API service

**PATH_PB** (optional): Path for source folder. Default path is /usr/src/app/pb. Regardless of using this parameter or not, you most mount this path.

**PATH_TAR** (optional): Path for target folder. Default path is /usr/src/app/tar. Regardless of using this parameter or not, you most mount this path.

### Program Execution (Independent Runtime)

```
docker run --rm -e "DATA_NAME=HART" -e "TIMEZONE=America/New_York" -v /transi/data/pb/hart:/usr/src/app/pb -v /transi/data/tar/hart:/usr/src/app/tar registry.gitlab.com/cutr-at-usf/transi/core/archive-pb
```

### Execution Parameters

**DATA_NAME**: Dataset Name. Used as tar.gz file prefix.

**TIMEZONE**: Used to accurately place PB files into the correct archive.

**PATH_PB** (optional): Path for source folder. Default path is /usr/src/app/pb. Regardless of using this parameter or not, you most mount this path.

**PATH_TAR** (optional): Path for target folder. Default path is /usr/src/app/tar. Regardless of using this parameter or not, you most mount this path.

Please refer to [getting started project](https://gitlab.com/cutr-at-usf/transi/core/getting-started) for more information about the system

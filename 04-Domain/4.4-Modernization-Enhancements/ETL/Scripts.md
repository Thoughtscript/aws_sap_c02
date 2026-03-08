# Scripts

## Libraries

There are several overlapping and independent libraries, tools, and skills:

1. `awsglue`
1. `botocore`
1. `pyspark`
1. `boto3`
1. Want to test using the official `public.ecr.aws/glue/aws-glue-libs:5` public Amazon AWS Documentation Docker Image.
1. Apache Spark
1. Hadoop
1. Java
1. Amazon AWS Glue ETL, EMR

> AWS Glue is mostly covered in the [AWS Certified Data Engineer - Associate](https://aws.amazon.com/certification/certified-data-engineer-associate/) learning path (and not the **AWS DevOps Pro** or **AWS Solutions Architect Pro** paths) but it's still useful to have some knowledge of these important libraries, tools, and skills.

## Use

Several ways to interact with this in shell:

1. `exec` into the **Container** through [REPL](https://docs.aws.amazon.com/glue/latest/dg/develop-local-docker-image.html#develop-local-docker-image-setup-run)

    ```bash
    docker run -it --rm \
        -v ~/.aws:/home/hadoop/.aws \
        -e AWS_PROFILE=test \
        --name glue5_pyspark \
        public.ecr.aws/glue/aws-glue-libs:5 \
        pyspark
    ```

1. `build` and do so:
    ```bash
    docker build .

    docker run -it --rm \
        -v ~/.aws:/home/hadoop/.aws \
        -e AWS_PROFILE=test \
        --name glue5_pyspark \
        MY_DOCKER_IMAGE_SHA \
        pyspark
    ```

1. `pull` and do so:
    ```bash
    docker pull public.ecr.aws/glue/aws-glue-libs:5 

    docker run -it --rm \
        -v ~/.aws:/home/hadoop/.aws \
        -e AWS_PROFILE=test \
        --name glue5_pyspark \
        MY_DOCKER_IMAGE_SHA \
        pyspark
    ```

1. Through `spark-submit`:
    ```bash
    docker run -it --rm \
        -v ~/.aws:/home/hadoop/.aws \
        -e AWS_PROFILE=test \
        --name glue5_pyspark \
        MY_DOCKER_IMAGE_SHA \
         spark-submit --num-executors 3 --driver-memory 512m --executor-memory 512m --executor-cores 1 boto-example.py
    ```

1. Through `spark-submit`:
    ```bash
    docker run -it --rm \
        -v ~/.aws:/home/hadoop/.aws \
        -e AWS_PROFILE=test \
        --name glue5_pyspark \
        MY_DOCKER_IMAGE_SHA \
         spark-submit --num-executors 3 --driver-memory 512m --executor-memory 512m --executor-cores 1 pyspark-example.py
    ```

1. Through `spark-submit`:
    ```bash
    docker run -it --rm \
        -v ~/.aws:/home/hadoop/.aws \
        -e AWS_PROFILE=test \
        --name glue5_pyspark \
        MY_DOCKER_IMAGE_SHA \
         spark-submit --num-executors 3 --driver-memory 512m --executor-memory 512m --executor-cores 1 boto3-pyspark-example.py
    ```

> Spinning up actual Amazon AWS Glue or AWS EMR resources can be expensive even for testing and its proven a bit tricky to find a *bona fide* AWS Cloud simulation/mock.

## Scripts

### Simple Job

```bash
$ pyspark
```

Through the official AWS REPL lab:

```python
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
import sys

# sys.argv must be used here not argparse
sys.argv += ['--JOB_NAME', 'example'] # arg flag passed here using comprehensions syntax
sys.argv += ['--JOB_RUN_ID', '1']
args = getResolvedOptions(sys.argv, ["JOB_NAME"]) # Chose the relevant ID
gc = GlueContext(sc)
job = Job(gc)
job.init(args["JOB_NAME"], args)
job.commit()

sc.stop()
```
```python
exit()
```

### Boto Client

This simulates using the `boto3` Client to interact with AWS Resources using `stubber` (a Mocking and Testing library from AWS Client calls). This is a very specific approach that attempts to do away with `boto3` configuration for a fully mocked client.

> For instance: the `~/.aws` credentials are completely faked - I haven't found a complete example with config doing this (that works on the internet so far). (`boto3` must have a config and it varies from the standard `aws-cli` configs...)

```python
# Example for pasting into Interactive Terminal Exec
import botocore.session
from botocore.stub import Stubber

glue_client = botocore.session.get_session().create_client('glue')
mock_response = {'Name': 'test-job-name','ResponseMetadata': {'HTTPStatusCode': 200} }
expected_params = {'Name': 'test-job-name','Role': 'arn:aws:iam::123456789012:role/test-role','Command': {'Name': 'glueetl', 'ScriptLocation': 's3://my-bucket/script.py'}}
stubber = Stubber(glue_client)
stubber.add_response('create_job', mock_response, expected_params)
stubber.activate()
response = glue_client.create_job(Name='test-job-name',Role='arn:aws:iam::123456789012:role/test-role',Command={'Name': 'glueetl', 'ScriptLocation': 's3://my-bucket/script.py'})
print(response) # {'Name': 'test-job-name', 'ResponseMetadata': {'HTTPStatusCode': 200}}
```
```python
exit()
```

The `boto3` Client can also be used with `Stubber`:

```python
glue_client = boto3.client("glue", "us-east-1")
stubber = Stubber(glue_client)
subber.activate()
```

```python
# Example for pasting into Interactive Terminal Exec
import boto3
import botocore.session
from botocore.stub import Stubber

glue_client = boto3.client("glue", "us-east-1")
stubber = Stubber(glue_client)
# Note sure what ISO Format but from timestamps generated through datetime.datetime
## hhttps://docs.aws.amazon.com/boto3/latest/reference/services/glue/client/get_job_run.html#
mock_response = {"JobRun":{"Id":"string","Attempt":123,"PreviousRunId":"string","TriggerName":"string","JobName":"string","JobMode":"SCRIPT","StartedOn":"2015-01-01 00:00:00","LastModifiedOn":"2015-01-01 00:00:00","CompletedOn":"2015-01-01 00:00:00","JobRunState":"SUCCEEDED","Arguments":{"string":"string"},"ErrorMessage":"string","PredecessorRuns":[{"JobName":"string","RunId":"string"}],"AllocatedCapacity":123,"ExecutionTime":123,"Timeout":123,"MaxCapacity":123,"WorkerType":"Standard","NumberOfWorkers":123,"SecurityConfiguration":"string","LogGroupName":"string","NotificationProperty":{"NotifyDelayAfter":123},"GlueVersion":"string","DPUSeconds":123,"ExecutionClass":"FLEX","MaintenanceWindow":"string","ProfileName":"string"}}
expected_params = { "JobName": "example-01", "RunId": "run-uuid-0000-0000-0000" }
stubber.add_response("get_job_run", mock_response, expected_params)
stubber.activate()

response = glue_client.get_job_run(JobName="example-01", RunId="run-uuid-0000-0000-0000")
print(response) # {'JobRun': {'Id': 'string', 'Attempt': 123, 'PreviousRunId': 'string', 'TriggerName': 'string', 'JobName': 'string', 'JobMode': 'SCRIPT', 'StartedOn': '2015-01-01 00:00:00', 'LastModifiedOn': '2015-01-01 00:00:00', 'CompletedOn': '2015-01-01 00:00:00', 'JobRunState': 'SUCCEEDED', 'Arguments': {'string': 'string'}, 'ErrorMessage': 'string', 'PredecessorRuns': [{'JobName': 'string', 'RunId': 'string'}], 'AllocatedCapacity': 123, 'ExecutionTime': 123, 'Timeout': 123, 'MaxCapacity': 123, 'WorkerType': 'Standard', 'NumberOfWorkers': 123, 'SecurityConfiguration': 'string', 'LogGroupName': 'string', 'NotificationProperty': {'NotifyDelayAfter': 123}, 'GlueVersion': 'string', 'DPUSeconds': 123, 'ExecutionClass': 'FLEX', 'MaintenanceWindow': 'string', 'ProfileName': 'string'}}
```

## References:
1. https://dev.to/515hikaru/practical-example-of-using-boto3-stubber-class-unit-tests-i5b
1. https://docs.aws.amazon.com/botocore/latest/reference/stubber.html
1. https://dev.to/cwprogram/python-aws-testing-with-boto-stubber-272k
1. https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html
1. https://docs.aws.amazon.com/code-library/latest/ug/python_3_glue_code_examples.html
1. https://aws.amazon.com/blogs/big-data/develop-and-test-aws-glue-5-0-jobs-locally-using-a-docker-container/
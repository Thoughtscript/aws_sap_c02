# Scripts

Couple ways to interact with this:

1. `exec` into the **Container** through [REPL](https://docs.aws.amazon.com/glue/latest/dg/develop-local-docker-image.html#develop-local-docker-image-setup-run)

    ```bash
    docker run -it --rm \
        -v ~/.aws:/home/hadoop/.aws \
        -e AWS_PROFILE=$PROFILE_NAME \
        --name glue5_pyspark \
        public.ecr.aws/glue/aws-glue-libs:5 \
        pyspark
    ```

1. `build` and do so:
    ```bash
    docker build .

    docker run -it --rm \
        -v ~/.aws:/home/hadoop/.aws \
        -e AWS_PROFILE=$PROFILE_NAME \
        --name glue5_pyspark \
        MY_DOCKER_IMAGE_ID \
        pyspark
    ```

1. `pull` and do so:
    ```bash
    docker pull public.ecr.aws/glue/aws-glue-libs:5 

    docker run -it --rm \
        -v ~/.aws:/home/hadoop/.aws \
        -e AWS_PROFILE=$PROFILE_NAME \
        --name glue5_pyspark \
        MY_DOCKER_IMAGE_ID \
        pyspark
    ```

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

### Boto Client

This simulates using the `boto3` Client to interact with AWS Resources using `stubber` (a Mocking and Testing library from AWS Client calls).

```python
import botocore.session
from botocore.stub import Stubber

    def create_glue_job(client, job_name, role_arn, command):
        response = client.create_job(
            Name=job_name,
            Role=role_arn,
            Command=command
        )
        return response['Name']

    glue_client = boto3.client('glue', rregion_name='us-west-2')

    mock_response = {
        'Name': 'test-job-name',
        'ResponseMetadata': {
            'HTTPStatusCode': 200
        }
    }
    expected_params = {
        'Name': 'test-job-name',
        'Role': 'arn:aws:iam::123456789012:role/test-role',
        'Command': {'Name': 'glueetl', 'ScriptLocation': 's3://my-bucket/script.py'}
    }
    
    with Stubber(glue_client) as stubber:
        # Stubbed and mocked calls
        stubber.add_response('create_job', mock_response, expected_params)

        job_name = create_glue_job(
            glue_client,
            'test-job-name',
            'arn:aws:iam::123456789012:role/test-role',
            {'Name': 'glueetl', 'ScriptLocation': 's3://my-bucket/script.py'}
        )

        assert job_name == 'test-job-name'
        
        stubber.assert_no_pending_responses()
```

References:
1. https://dev.to/515hikaru/practical-example-of-using-boto3-stubber-class-unit-tests-i5b
1. https://docs.aws.amazon.com/botocore/latest/reference/stubber.html
1. https://dev.to/cwprogram/python-aws-testing-with-boto-stubber-272k

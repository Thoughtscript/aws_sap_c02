import boto3
import botocore.session
from botocore.stub import Stubber

if __name__ == '__main__':

    try:

        glue_client = boto3.client("glue", "us-east-1")
        stubber = Stubber(glue_client)
        # Note sure what ISO Format but from timestamps generated through datetime.datetime
        ## https://docs.aws.amazon.com/boto3/latest/reference/services/glue/client/get_job_run.html
        ## The JSON response must still conform to the expected value in boto3 (even though it's intercepted and mocked by botocore)!
        ### Otherwise it'll throw: 
        #### Exception: Parameter validation failed:
        #### Unknown parameter in input: "job", must be one of: Job
        mock_response = {"JobRun":{"Id":"string","Attempt":123,"PreviousRunId":"string","TriggerName":"string","JobName":"string","JobMode":"SCRIPT","StartedOn":"2015-01-01 00:00:00","LastModifiedOn":"2015-01-01 00:00:00","CompletedOn":"2015-01-01 00:00:00","JobRunState":"SUCCEEDED","Arguments":{"string":"string"},"ErrorMessage":"string","PredecessorRuns":[{"JobName":"string","RunId":"string"}],"AllocatedCapacity":123,"ExecutionTime":123,"Timeout":123,"MaxCapacity":123,"WorkerType":"Standard","NumberOfWorkers":123,"SecurityConfiguration":"string","LogGroupName":"string","NotificationProperty":{"NotifyDelayAfter":123},"GlueVersion":"string","DPUSeconds":123,"ExecutionClass":"FLEX","MaintenanceWindow":"string","ProfileName":"string"}}
        expected_params = { "JobName": "example-01", "RunId": "run-uuid-0000-0000-0000" }
        stubber.add_response("get_job_run", mock_response, expected_params)
        stubber.activate()

        response = glue_client.get_job_run(JobName="example-01", RunId="run-uuid-0000-0000-0000")
        print(response) # {'JobRun': {'Id': 'string', 'Attempt': 123, 'PreviousRunId': 'string', 'TriggerName': 'string', 'JobName': 'string', 'JobMode': 'SCRIPT', 'StartedOn': '2015-01-01 00:00:00', 'LastModifiedOn': '2015-01-01 00:00:00', 'CompletedOn': '2015-01-01 00:00:00', 'JobRunState': 'SUCCEEDED', 'Arguments': {'string': 'string'}, 'ErrorMessage': 'string', 'PredecessorRuns': [{'JobName': 'string', 'RunId': 'string'}], 'AllocatedCapacity': 123, 'ExecutionTime': 123, 'Timeout': 123, 'MaxCapacity': 123, 'WorkerType': 'Standard', 'NumberOfWorkers': 123, 'SecurityConfiguration': 'string', 'LogGroupName': 'string', 'NotificationProperty': {'NotifyDelayAfter': 123}, 'GlueVersion': 'string', 'DPUSeconds': 123, 'ExecutionClass': 'FLEX', 'MaintenanceWindow': 'string', 'ProfileName': 'string'}}

    except Exception as ex:

        print('Exception: ' + str(ex))

'''
Flattened:

# Example for pasting into Interactive Terminal Exec
import boto3
import botocore.session
from botocore.stub import Stubber

glue_client = boto3.client("glue", "us-east-1")
stubber = Stubber(glue_client)
mock_response = {"JobRun":{"Id":"string","Attempt":123,"PreviousRunId":"string","TriggerName":"string","JobName":"string","JobMode":"SCRIPT","StartedOn":"2015-01-01 00:00:00","LastModifiedOn":"2015-01-01 00:00:00","CompletedOn":"2015-01-01 00:00:00","JobRunState":"SUCCEEDED","Arguments":{"string":"string"},"ErrorMessage":"string","PredecessorRuns":[{"JobName":"string","RunId":"string"}],"AllocatedCapacity":123,"ExecutionTime":123,"Timeout":123,"MaxCapacity":123,"WorkerType":"Standard","NumberOfWorkers":123,"SecurityConfiguration":"string","LogGroupName":"string","NotificationProperty":{"NotifyDelayAfter":123},"GlueVersion":"string","DPUSeconds":123,"ExecutionClass":"FLEX","MaintenanceWindow":"string","ProfileName":"string"}}
expected_params = { "JobName": "example-01", "RunId": "run-uuid-0000-0000-0000" }
stubber.add_response("get_job_run", mock_response, expected_params)
stubber.activate()

response = glue_client.get_job_run(JobName="example-01", RunId="run-uuid-0000-0000-0000")
print(response)
'''
import botocore.session
from botocore.stub import Stubber

if __name__ == '__main__':

    try:

        def create_glue_job(client, job_name, role_arn, command):
            response = client.create_job(
                Name=job_name,
                Role=role_arn,
                Command=command
            )
            return response['Name']

        glue_client = botocore.session.get_session().create_client('glue')

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

    except Exception as ex:

        print('Exception: ' + str(ex))
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
import sys

if __name__ == '__main__':

    try:

        # sys.argv must be used here not argparse
        sys.argv += ['--JOB_NAME', 'example'] # arg flag passed here using comprehensions syntax
        sys.argv += ['--JOB_RUN_ID', '1'] # this must also be present or errors thrown
        args = getResolvedOptions(sys.argv, ["JOB_NAME"]) # Chose the relevant ID
        gc = GlueContext(sc)
        job = Job(gc)
        job.init(args["JOB_NAME"], args)
        job.commit()

        sc.stop()

    except Exception as ex:

        print('Exception: ' + str(ex))
import botocore.client
import json
from typing import Callable

from plenario_stream_core.signals import job_created

from .defaults import KINESIS_STREAM, PARTITION_KEY


def add_job_created_handler(kinesis: botocore.client.BaseClient) -> Callable:
    """Add a handler for the signals emitted by models that represent etl jobs.
    A set of these models is provided by the plenario_stream_core package.
    """
    def job_created_handler(**kwargs) -> dict:
        """Using information from the `job_created` signal, enqueue a payload
        onto Kinesis.
        """
        job = kwargs['instance']
        return kinesis.put_record(
            StreamName=KINESIS_STREAM,
            PartitionKey=PARTITION_KEY,
            Data=json.dumps({
                'id': job.id,
                'table': job.ds_name,
                'columns': job.ds_fields,
                'rows': job.payload,
            }).encode(),
        )
    job_created.connect(job_created_handler)
    return job_created_handler

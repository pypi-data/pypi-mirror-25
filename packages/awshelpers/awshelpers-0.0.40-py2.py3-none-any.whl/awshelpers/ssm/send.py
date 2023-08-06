from awshelpers.ssm import _connect
from typing import List, Optional


def command(instance_ids: List[str], document_name: str, timeout: int, comment: str, commands: List[str],
            s3_region: Optional[str],
            s3_bucket: Optional[str], s3_prefix: Optional[str]) -> dict:
    """
    Sends a command to SSM.

    Args:
        instance_ids: A list of instance ids.
        document_name: The name of an existing AWS Command docment or a custom document.
        timeout: Timeout in seconds for command to run.
        comment: A comment, useful when parsing large lists of commands.
        commands: A list of commands to run.
        s3_region: Deprecated, SSM automatically determines this.
        s3_bucket: The name of the S3 bucket to store command output in.
        s3_prefix (): The prefix to use within the S3 bucket.

    Returns:

    """
    return _connect.client().send_command(
        InstanceIds=instance_ids,
        DocumentName=document_name,
        TimeoutSeconds=timeout,
        Comment=comment,
        Parameters={
            'commands': commands
        },
        OutputS3Region=s3_region,
        OutputS3BucketName=s3_bucket,
        OutputS3KeyPrefix=s3_prefix,
    )

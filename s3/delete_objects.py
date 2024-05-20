import logging
import boto3
from botocore.exceptions import ClientError  # Import ClientError


def delete_objects(bucket, object_keys):
    """
    Removes a list of objects from a bucket.
    This operation is done as a batch in a single request.

    :param bucket: The bucket that contains the objects. This is a Boto3 Bucket
                   resource.
    :param object_keys: The list of keys that identify the objects to remove.
    :return: The response that contains data about which objects were deleted
             and any that could not be deleted.
    """
    logger = logging.getLogger(__name__)

    try:
        response = bucket.delete_objects(
            Delete={"Objects": [{"Key": key} for key in object_keys]}
        )
        if "Deleted" in response:
            logger.info(
                "Deleted objects '%s' from bucket '%s'.",
                [del_obj["Key"] for del_obj in response["Deleted"]],
                bucket.name,
            )
        if "Errors" in response:
            logger.warning(
                "Could not delete objects '%s' from bucket '%s'.",
                [
                    f"{del_obj['Key']}: {del_obj['Code']}"
                    for del_obj in response["Errors"]
                ],
                bucket.name,
            )
    except ClientError:
        logger.exception("Couldn't delete any objects from bucket %s.", bucket.name)
        raise
    else:
        return response


# Example usage
s3 = boto3.resource('s3')
bucket = s3.Bucket('anothernewbucketface')
delete_objects(bucket, ['sdhfuehfus'])

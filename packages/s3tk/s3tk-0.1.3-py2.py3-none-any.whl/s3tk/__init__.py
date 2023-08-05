import sys
import os.path
import json
import fnmatch
import boto3
import botocore
import click
from joblib import Parallel, delayed
from clint.textui import colored, puts, indent
from .checks import AclCheck, PolicyCheck, LoggingCheck, VersioningCheck

__version__ = '0.1.3'

s3 = boto3.resource('s3')


def notice(message):
    puts(colored.yellow(message))


def abort(message):
    puts(colored.red(message))
    sys.exit(1)


def perform(check):
    check.perform()

    with indent(2):
        if check.status == 'passed':
            puts(colored.green(check.name + ' ' + check.pass_message))
        elif check.status == 'failed':
            puts(colored.red(check.name + ' ' + check.fail_message))
        else:
            puts(colored.red(check.name + ' access denied'))

    return check


def fetch_buckets(buckets):
    if buckets:
        if any("*" in b for b in buckets):
            return [b for b in s3.buckets.all() if any(fnmatch.fnmatch(b.name, bn) for bn in buckets)]
        else:
            return [s3.Bucket(bn) for bn in buckets]
    else:
        return s3.buckets.all()


def fix_check(klass, buckets, dry_run, fix_args={}):
    try:
        for bucket in fetch_buckets(buckets):
            check = klass(bucket)
            check.perform()

            if check.status == 'passed':
                message = colored.green('already enabled')
            elif check.status == 'denied':
                message = colored.red('access denied')
            else:
                if dry_run:
                    message = colored.yellow('to be enabled')
                else:
                    try:
                        check.fix(fix_args)
                        message = colored.blue('just enabled')
                    except botocore.exceptions.ClientError as e:
                        message = colored.red(str(e))

            puts(bucket.name + ' ' + message)

    # can't list buckets
    except (botocore.exceptions.ClientError, botocore.exceptions.NoCredentialsError) as e:
        abort(str(e))


def encrypt_object(bucket_name, key, dry_run, kms_key_id, customer_key):
    obj = s3.Object(bucket_name, key)

    try:
        if customer_key:
            obj.load(SSECustomerAlgorithm='AES256', SSECustomerKey=customer_key)

        encrypted = None
        if customer_key:
            encrypted = obj.sse_customer_algorithm is not None
        elif kms_key_id:
            encrypted = obj.server_side_encryption == 'aws:kms'
        else:
            encrypted = obj.server_side_encryption == 'AES256'

        if encrypted:
            puts(obj.key + ' ' + colored.green('already encrypted'))
        else:
            if dry_run:
                puts(obj.key + ' ' + colored.yellow('to be encrypted'))
            else:
                copy_source = {'Bucket': bucket_name, 'Key': obj.key}

                # TODO support going from customer encryption to other forms
                if kms_key_id:
                    obj.copy_from(
                        CopySource=copy_source,
                        ServerSideEncryption='aws:kms',
                        SSEKMSKeyId=kms_key_id
                    )
                elif customer_key:
                    obj.copy_from(
                        CopySource=copy_source,
                        SSECustomerAlgorithm='AES256',
                        SSECustomerKey=customer_key
                    )
                else:
                    obj.copy_from(
                        CopySource=copy_source,
                        ServerSideEncryption='AES256'
                    )

                puts(obj.key + ' ' + colored.blue('just encrypted'))

    except (botocore.exceptions.ClientError, botocore.exceptions.NoCredentialsError) as e:
        puts(obj.key + ' ' + colored.red(str(e)))


def reset_object(bucket_name, key, dry_run):
    obj = s3.Object(bucket_name, key)

    try:
        if dry_run:
            puts(obj.key + ' ' + colored.yellow('ACL to be reset'))
        else:
            obj.Acl().put(ACL='private')
            puts(obj.key + ' ' + colored.blue('ACL reset'))

    except (botocore.exceptions.ClientError, botocore.exceptions.NoCredentialsError) as e:
        puts(obj.key + ' ' + colored.red(str(e)))


@click.group()
@click.version_option(version=__version__)
def cli():
    pass


@cli.command()
@click.argument('buckets', nargs=-1)
@click.option('--skip-logging', is_flag=True, help='Skip logging check')
@click.option('--skip-versioning', is_flag=True, help='Skip versioning check')
def scan(buckets, skip_logging=False, skip_versioning=False):
    checks = []

    try:
        for bucket in fetch_buckets(buckets):
            puts(bucket.name)

            checks.append(perform(AclCheck(bucket)))

            checks.append(perform(PolicyCheck(bucket)))

            if not skip_logging:
                checks.append(perform(LoggingCheck(bucket)))

            if not skip_versioning:
                checks.append(perform(VersioningCheck(bucket)))

            puts()

        if sum(1 for c in checks if c.status != 'passed') > 0:
            sys.exit(1)

    # can't list buckets
    except (botocore.exceptions.ClientError, botocore.exceptions.NoCredentialsError) as e:
        abort(str(e))


@cli.command(name='enable-logging')
@click.argument('buckets', nargs=-1)
@click.option('--dry-run', is_flag=True, help='Dry run')
@click.option('--log-bucket', required=True, help='Bucket to store logs')
def enable_logging(buckets, log_bucket=None, dry_run=False):
    fix_check(LoggingCheck, buckets, dry_run, {'log_bucket': log_bucket})


@cli.command(name='enable-versioning')
@click.argument('buckets', nargs=-1)
@click.option('--dry-run', is_flag=True, help='Dry run')
def enable_versioning(buckets, dry_run=False):
    fix_check(VersioningCheck, buckets, dry_run)


@cli.command()
@click.argument('bucket')
@click.option('--dry-run', is_flag=True, help='Dry run')
@click.option('--kms-key-id', help='KMS key id')
@click.option('--customer-key', help='Customer key')
def encrypt(bucket, dry_run=False, kms_key_id=None, customer_key=None):
    try:
        bucket = s3.Bucket(bucket)

        Parallel(n_jobs=10, backend="threading")(delayed(encrypt_object)(bucket.name, os.key, dry_run, kms_key_id, customer_key) for os in bucket.objects.all())

    except (botocore.exceptions.ClientError, botocore.exceptions.NoCredentialsError) as e:
        abort(str(e))


@cli.command(name='reset-object-acl')
@click.argument('bucket')
@click.option('--dry-run', is_flag=True, help='Dry run')
def reset_object_acl(bucket, dry_run=False):
    try:
        bucket = s3.Bucket(bucket)

        Parallel(n_jobs=10, backend="threading")(delayed(reset_object)(bucket.name, os.key, dry_run) for os in bucket.objects.all())

    except (botocore.exceptions.ClientError, botocore.exceptions.NoCredentialsError) as e:
        abort(str(e))


@cli.command(name='list-policy')
@click.argument('buckets', nargs=-1)
def list_policy(buckets):
    try:
        for bucket in fetch_buckets(buckets):
            puts(bucket.name)

            policy = None
            try:
                policy = bucket.Policy().policy
            except botocore.exceptions.ClientError as e:
                if 'NoSuchBucket' not in str(e):
                    raise

            with indent(2):
                if policy is None:
                    puts(colored.yellow("None"))
                else:
                    puts(colored.yellow(json.dumps(json.loads(policy), indent=4)))

            puts()

    except (botocore.exceptions.ClientError, botocore.exceptions.NoCredentialsError) as e:
        abort(str(e))

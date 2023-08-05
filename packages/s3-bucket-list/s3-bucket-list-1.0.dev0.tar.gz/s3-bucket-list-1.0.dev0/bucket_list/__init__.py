
import click
import datetime
from subprocess import check_output
import boto.ec2
from boto.ec2.blockdevicemapping import BlockDeviceMapping
from boto.ec2.blockdevicemapping import BlockDeviceType
import boto.ec2.networkinterface
import boto.route53
from boto.s3.connection import Location
from boto.s3.connection import S3Connection
from boto.ec2.cloudwatch import CloudWatchConnection
from datetime import datetime, timedelta
from commons import *
from tbvaccine import TBVaccine
import tbvaccine
from commons.Table import Table
import json
import xml.etree.ElementTree

tbvaccine.add_hook(isolate=False)

def format_policy(p):
    s = p["Action"] + ":"
    for k,v in p["Principal"].iteritems():
      s += k + "->" + v + " "
    return s if p["Effect"] == "Allow" else "!" + s

def format_acl(acl):
    # print green(acl)
    if acl is None or acl == "":
        return ""
    s = ""
    root = xml.etree.ElementTree.fromstring(acl)
    if "AccessControlList" not in root:
        # print red(str(root.keys()))
        return ""
    for grant in root.find("AccessControlList").findall('Grant'):
        grantee = grant.find("Grantee")
        if grantee.find("DisplayName") is not None:
            s += grantee.find("DisplayName").text + "->"
        elif grantee.find("URI") is not None:
            s += grantee.find("URI").text.replace("http://acs.amazonaws.com/groups/global/", "") + "->"
        else:
            s += ""
        s += grant.find("Permission").text + " "
    return s


def get_by_prefix(_bucket, prefix):
    max = None
    count = 0
    size = 0
    for key in _bucket.list(prefix=prefix):
        count += 1
        size += key.size
        if not ".zip" in key.name:
            continue
        if max is None or max.last_modified < key.last_modified:
            max = key
    return (max, count, size)

def get_policies(s3_bucket):
    policy = ""
    try:
        policy = s3_bucket.get_policy()
        policy = json.loads(policy)["Statement"]
        policy = ",".join([format_policy(p) for p in policy])
    except:
        pass
    try:
        policy += format_acl(s3_bucket.get_acl().to_xml())
    except Exception, e:
        print(TBVaccine().format_exc())

    for key in s3_bucket.get_all_keys(max_keys=1):
        for acl in key.get_acl().acl.grants:
            if acl.type == 'Group':
                policy += "%s => %s " % (acl.uri.split("/")[-1], acl.permission)
            elif acl.type == 'CanonicalUser':
                policy += "%s => %s " % (acl.display_name, acl.permission)
            else:
                policy += str(acl.__dict__)
    return policy

def get_lifecycles(s3_bucket):
    try:
        s3_bucket.get_lifecycle_config()
        if lifecycle is not None:
            return lifecycle.to_xml()
    except:
        pass
    return

def get_versioning(s3_bucket):
    _versioning = s3_bucket.get_versioning_status()
    versioning = "true" if _versioning["Versioning"] == "Enabled" else "false"
    mfa = "true" if "MFADelete" in _versioning and _versioning["MFADelete"] == "Enabled" else "false"
    return (versioning, mfa)


def query_buckets(get_lifecycle=False, get_policy=False, prefix=None, status=None):
    status.update_status("Querying buckets .. ")
    s3 = S3Connection(is_secure=False)
    for region in boto.ec2.cloudwatch.regions():
        client = boto.ec2.cloudwatch.connect_to_region(region.name)
        start = datetime.now() - timedelta(hours=24 * 7)
        try:
            for metric in client.list_metrics(metric_name='BucketSizeBytes'):
                bucket = metric.dimensions["BucketName"][0]
                status.update_status(bucket)
                try:
                    size = metric.query(start, datetime.now(), ['Average'], 'Bytes', period=86400)[0]["Average"]
                    dimensions =  metric.dimensions
                    dimensions["StorageType"] = ["AllStorageTypes"]
                    objects = client.get_metric_statistics(86400, start, datetime.now(),
                         'NumberOfObjects', metric.namespace, ['Average'], dimensions, None)
                    diff = objects[len(objects) - 1]["Average"] - objects[0]["Average"]
                    diff = diff/len(objects)

                    s3_bucket = s3.get_bucket(bucket)
                    lifecycle = get_lifecycles(s3_bucket) if get_lifecycle else ""
                    policy = get_policies(s3_bucket) if get_policy else ""
                    (versioning, mfa) = get_versioning(s3_bucket)

                    details = {}
                    if prefix is not None:
                        status.update_status("Querying %s/%s" % (bucket, prefix))
                        (max, count, prefix_size) = get_by_prefix(s3_bucket, prefix)
                        details[prefix + "_size"] = prefix_size
                        details[prefix + "_count"] = count
                        if max is not None:
                            details[prefix + "_age"] = get_age_in_seconds(max.last_modified)
                            details[prefix] = max.name + " (" + format_bytes(max.size) + ")"

                    details.update({
                        "bucket": bucket,
                        "region": region.name,
                        "size": size,
                        "count": objects[0]["Average"],
                        "versioning": versioning,
                        "mfa": mfa,
                        "lifecycle": lifecycle,
                        "policy": policy
                        # "rate": diff
                    })
                    yield details
                except Exception, e:
                    print(TBVaccine().format_exc())
                    yield {
                        "bucket": bucket
                    }
        except:
             print(TBVaccine().format_exc())



@click.command()
@click.option('--lifecycle', default=False,  is_flag=True)
@click.option('--policies', default=False,  is_flag=True)
@click.option('--prefix')
def main(lifecycle, policies, prefix):
    columns = [
        {"name": "bucket", "width": 30},
        {"name": "size", "width": 20, "type": "size"},
        {"name": "count", "width": 20, "type": "number"},
        {"name": "versioning", "type": "boolean"},
        {"name": "mfa", "type": "boolean"}]
    if prefix is not None:
        columns += [
            {"name": prefix + "_size", "type": "size"},
            {"name": prefix + "_count", "type": "number"},
            {"name": prefix + "_age",  "type": "age"},
            {"name": prefix}
        ]

    if lifecycle:
        columns.append({"name": "lifecycle"})
    if policies:
        columns.append({"name": "policy"})
    table = Table(columns=columns)
    for bucket in query_buckets(lifecycle, policies, prefix, table):
        table.append(bucket)




if __name__ == '__main__':
    cli()
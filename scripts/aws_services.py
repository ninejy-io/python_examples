import os
import sys
import time
import boto3


class S3Bucket:
    client = boto3.client('s3')
    __s3 = boto3.resource('s3')

    def create_bucket(self, **kwargs):
        '''
        ACL='private'|'public-read'|'public-read-write'|'authenticated-read',
        Bucket='string',
        CreateBucketConfiguration={
            'LocationConstraint': 'EU'|'eu-west-1'|'us-west-1'|'us-west-2'|'ap-south-1'|'ap-southeast-1'
                                  'ap-southeast-2'|'ap-northeast-1'|'sa-east-1'|'cn-north-1'|'eu-central-1'
        },
        GrantFullControl='string',
        GrantRead='string',
        GrantReadACP='string',
        GrantWrite='string',
        GrantWriteACP='string'
        '''
        res = self.client.create_bucket(**kwargs)
        print(res)

    @classmethod
    def list_all_buckets(cls):
        res = cls.client.list_buckets()
        # print(res)
        return [bucket['Name'] for bucket in res['Buckets']]

    def bucket_access_control(self, bucket):
        bucket = self.__s3.Bucket(bucket)
        bucket.AcL().put(ACL='public-read')

        acl = bucket.Acl()
        print(acl.grants)

    def set_cors(self, bucket):
        bucket = self.__s3.Bucket(bucket)
        cors = bucket.Cors()
        config = {
            'CORSRules': [
                {
                    'AllowedMethods': ['GET', 'HEAD', 'OPTIONS'],
                    'AllowedOrigins': ['*']
                }
            ]
        }
        cors.put(CORSConfiguation=config)
        
        cors.delete()

    def list_all_objects(self, **kwargs):
        '''
        Bucket='string',
        Delimiter='string',
        EncodingType='url',
        Marker='string',
        MaxKeys=123,
        Prefix='string',
        RequestPayer='requester'
        '''
        res = self.client.list_objects(**kwargs)
        for obj in res['Contents']:
            print(obj, type(obj))

    def upload_file(self, filepath, bucket, name):
        self.__s3.meta.client.upload_file(filepath, bucket, name)

    def object_access_control(self, bucket, object_name):
        object_acl = self.__s3.ObjectAcl(bucket, object_name)
        object_acl.put(ACL='public-read')


class CloudFront:
    client = boto3.client('cloudfront')

    def create_distribution(self, **kwargs):
        pass

    def list_all_distributions(self):
        res = self.client.list_distributions()
        print(res)

    def create_invalidation(self, num, obj_lists, DisId="E3NIZHYMH7MSU0"):
        InvBatch = {
            'Paths': {
                'Quantity': num,
                'Items': obj_lists,
            },
            'CallerReference': str(time.time())
        }
        res = self.client.create_invalidation(
            DistributionId=DisId, InvalidationBatch=InvBatch)
        print("The invalidation id is --------------:", res['Invalidation']['Id'])        


if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        print("Where is your file directory ???")
        sys.exit(1)
    basedir = sys.argv[1]
    bucket_name = "test-bucket"
    bucket = S3Bucket()
    cf = CloudFront()

    fs = []
    new_names = []
    os.chdir(basedir)
    for root, dirs, files in os.walk('.'):
        if root == ".":
            fs.extend([f for f in files])
            new_names.extend('/{}'.format(f) for f in files)
        else:
            fs.extend(['{}/{}'.format(root.lstrip('./').lstrip('.\\'), f) for f in files])
            new_names.extend(['/{}/{}'.format(root.lstrip('./').lstrip('.\\'), f) for f in files])

    for fn in fs:
        print("uploading file -------------:", fn)
        bucket.upload_file(fn, bucket_name, fn)
        bucket.object_access_control(bucket_name, fn)

    cf.create_invalidation(len(new_names), new_names)


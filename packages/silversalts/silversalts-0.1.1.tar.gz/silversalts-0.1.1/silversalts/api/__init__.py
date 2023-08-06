
def ocr(spec, user, secret, host='api.silversalts.com', protocol='https'):
    import json
    import time
    import boto3
    import requests
    import botocore.exceptions

    from .crypter import SymmetricCrypter
    from .packager import SilverSaltsPackager


    def s3_file_exists(s3, bucket, key):
        exists = False
        try:
            s3.head_object(Bucket=bucket, Key=key)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                exists = False
            else:
                raise
        else:
            exists = True
        return exists

    if isinstance(secret, str):
        symmetric_crypter = SymmetricCrypter()
    else:
        raise NotImplementedError('secret must be an ascii string')
    ss_packager = SilverSaltsPackager(symmetric_crypter)
    url = '%s://%s/service/ocr' % (protocol, host, )
    res = requests.post(
        url,
        headers={
            'user': user,
        },
        data=ss_packager.pack(spec, secret)
    )
    if res.status_code == 200:
        result = ss_packager.unpack(res.content, secret)
        if result['output_scheme'] == spec['output_scheme']:
            if result['input_scheme'] == 'raw':
                return result['data']
            elif result['input_scheme'] == 's3':
                desc = json.loads(result['data'])
                s3 = boto3.Session(desc['access'], desc['secret']).client("s3")
                for i in range(desc['retry'] + 1):
                    if s3_file_exists(s3, desc['bucket'], desc['key']):
                        return s3.get_object(
                            Bucket=desc['bucket'],
                            Key=desc['key']
                        )['Body'].read()
                    else:
                        time.sleep(desc['sleep'])
        raise ValueError('Data returned from server is suspicious. Abandoning it for your safety.')
    raise SystemError('Server went wrong: %s - %s' % (res.status_code, res.text, ))

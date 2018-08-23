import boto3
import zipfile
import StringIO
import mimetypes

s3 = boto3.resource('s3')
resume_bucket = s3.Bucket('seanfaria.com')
build_bucket = s3.Bucket('codebuild.seanfaria.com')


resume_zip = StringIO.StringIO()
build_bucket.download_fileobj('ResumeBuild.zip',resume_zip)

with zipfile.ZipFile(resume_zip) as myzip:
    for nm in myzip.namelist():
     obj = myzip.open(nm)
     resume_bucket.upload_fileobj(obj, nm,
        ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
     resume_bucket.Object(nm).Acl().put(ACL='public-read')
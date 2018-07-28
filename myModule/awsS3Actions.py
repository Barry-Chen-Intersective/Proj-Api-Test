import boto3, json, os, constants


class awsS3Actions(object):

    def setup(self):
        self.userJson = {
            "AWS_ACCESS_KEY_ID" : os.environ["AWS_ACCESS_KEY_ID"],
            "AWS_SECRET_ACCESS_KEY" : os.environ["AWS_SECRET_ACCESS_KEY"],
            "REGION_NAME" : os.environ["REGION_NAME"],
            "AWS_S3_BUCKET" : os.environ["AWS_S3_BUCKET"]
        }

    def __init__(self):
        self.setup()
        if os.environ["PRD"] == "0":
            self.s3Client = boto3.client('s3', aws_access_key_id = self.userJson["AWS_ACCESS_KEY_ID"],
                                aws_secret_access_key = self.userJson["AWS_SECRET_ACCESS_KEY"],
                                region_name = self.userJson["REGION_NAME"])
        else:
            self.s3Client = boto3.client('s3', region_name = self.userJson["REGION_NAME"])
    
    def getS3JsonObject(self, objectKey):
        message = constants.SUCCESS
        try:
            s3Obj = self.s3Client.get_object(Bucket = self.userJson["AWS_S3_BUCKET"], Key = objectKey)
        except Exception:
            message = "Error on getting s3 object {}".format(objectKey)
            print message
            return message, {"data" : []}
        s3ObjBody = None
        jsonObj = None
        try:
            s3ObjBody = s3Obj["Body"]
            jsonObj = json.loads(s3ObjBody.read())
        finally:
            if s3ObjBody != None:
                s3ObjBody.close()
        return message, jsonObj
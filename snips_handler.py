from botocore.exceptions import ClientError
from snips_nlu import SnipsNLUEngine


class SnipsHandler:
    def __init__(self, id_account, id_agent, name, language, bucket):
        self.id_account = id_account
        self.id_agent = id_agent
        self.name = name
        self.language = language
        self.bucket = bucket
        self.key = self.id_account + "/" + self.id_agent + "/" + self.name + "_" + self.language + ".bot"
        self.snips = None

    def get_snips(self, s3, config):
        if self.snips is None:
            try:
                obj = s3.Object(self.bucket, self.key)
                body = obj.get()['Body'].read()
                self.snips = SnipsNLUEngine.from_byte_array(body)
            except ClientError as e:
                self.snips = SnipsNLUEngine(config=config)
            return self.get_snips(s3, config)
        else:
            return self.snips

    def save(self, s3, bucket):
        if self.snips is not None:
            trained_model = self.snips.to_byte_array()
            s3.put_object(Bucket=self.bucket,
                          Key=self.key,
                          Body=trained_model)

try:
    import unzip_requirements
except ImportError:
    pass
import json
import os
import load_languages
import boto3
from snips_nlu import load_resources
from snips_nlu.default_configs import CONFIG_EN, CONFIG_PT_BR

from snips_handler import SnipsHandler

load_languages.run()
bucket_name = os.getenv('MODEL_BUCKET_NAME', "")


def handler(event, context):
    model = event.get('body', event)
    if type(model) == str:
        model = json.loads(model)

    name = model.get("name")
    id_account = model.get("id_account")
    id_agent = model.get("id_agent")
    data = model.get("data")
    language = data.get("language")

    if language == "pt_br":
        config = CONFIG_PT_BR
    elif language == 'en':
        config = CONFIG_EN
    else:
        raise Exception("Language not supported: {}".format(language))

    load_resources(language)

    hand = SnipsHandler(id_account, id_agent, name, language, bucket_name)

    snips = hand.get_snips(boto3.resource('s3'), config)
    snips.fit(model.get("data"))
    hand.save(boto3.client('s3'), bucket_name)

    return {
        "statusCode": 200,
        "body": json.dumps({"status": "ok"})
    }

import os
import logging
import json
from pydantic import BaseSettings, AnyHttpUrl
from botocore.session import get_session

logger = logging.getLogger(__name__)


class CommonSetting(BaseSettings):
    BASE_DOMAIN: AnyHttpUrl = os.environ.get('BASE_DOMAIN', 'http://localhost')
    AWS_ACCESS_KEY: str = os.environ.get('AWS_ACCESS_KEY', '')
    AWS_SECRET_KEY: str = os.environ.get('AWS_SECRET_KEY', '')
    AWS_DEFAULT_REGION: str = os.environ.get('AWS_DEFAULT_REGION', '')
    AWS_SECRET_FILE: str = os.environ.get('AWS_SECRET_FILE', '')
    DATABASES_CONFIG = {
        "connections": {"default": os.environ['DATABASE_URL']},
        "apps": {
            "models": {
                "models": ["__main__"],
                "default_connection": "master",
            }
        },
        "use_tz": False,
        "timezone": "UTC",
    }

    class Config:
        @classmethod
        def customise_sources(
                cls,
                init_settings,
                env_settings,
                file_secret_settings,
        ):
            aws_access_key = os.environ.get('AWS_ACCESS_KEY', '')
            aws_secret_key = os.environ.get('AWS_SECRET_KEY', '')
            secret_name = os.environ.get('AWS_SECRET_FILE', '')
            if aws_access_key and aws_secret_key:
                session = get_session()
                client = session.create_client(
                    'secretsmanager', region_name='us-east-1',
                    aws_secret_access_key=aws_secret_key, aws_access_key_id=aws_access_key
                )
                secrets: dict = json.loads(client.get_secret_value(SecretId=secret_name)['SecretString'])
                for secret_key, value in secrets.items():
                    init_settings.init_kwargs[secret_key] = json.loads(value)
            return (
                init_settings,
                env_settings,
                file_secret_settings,
            )

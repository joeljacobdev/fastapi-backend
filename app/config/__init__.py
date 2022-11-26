import os

env_config_map = {
    'local': 'app.config.local',
    'deploy': 'app.config.deploy',
}


def get_config():
    env = os.environ.get('ENVIRONMENT', 'local')
    return env_config_map[env]

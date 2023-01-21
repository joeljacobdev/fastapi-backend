import os

env_config_map = {
    'local': 'app.settings.local',
    'deploy': 'app.settings.deploy',
}


def get_settings():
    env = os.environ.get('ENVIRONMENT', 'local')
    return env_config_map[env]

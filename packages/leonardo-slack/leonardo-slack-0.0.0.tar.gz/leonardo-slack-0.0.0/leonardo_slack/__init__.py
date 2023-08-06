
from django.apps import AppConfig
from django_slack import slack_message as default_slack_message


default_app_config = 'leonardo_slack.Config'


LEONARDO_APPS = ['leonardo_slack', 'django_slack']

LEONARDO_OPTGROUP = 'slack'

LEONARDO_CONFIG = {
    'SLACK_TOKEN': ('slack_token', 'Slack token'),
    'SLACK_CHANNEL': ('#general', 'Default slack channel'),
    'SLACK_USERNAME': ('leonardo', 'Slack bot username'),
    'SLACK_AS_USER': (False, 'Use this setting to set post '
                      'the message as the authed bot user or a bot.'),
    'SLACK_ICON_URL': ('', 'Slack icon url'),
}


class Config(AppConfig):
    name = 'leonardo_slack'
    verbose_name = "leonardo-slack"


def slack_message(message=None, username=None, channel=None,
                  template=None, context={}, **kwargs):
    if message:
        context['message'] = message
    if channel:
        context['channel'] = channel
    if username:
        context['username'] = username
    return default_slack_message(template or 'slack/base.slack', context)

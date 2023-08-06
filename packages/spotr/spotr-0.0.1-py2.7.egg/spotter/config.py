import ami
import boto3
from botocore.configloader import raw_config_parse


class Config:
    def __init__(self, client, args):
        self._config = raw_config_parse("~/.spotter/config")['config']
        self._config.update({k: v for k, v in vars(args).iteritems() if v})
        if 'ami' not in self._config and 'ami_tag' in self._config:
            ami_tag = self._config['ami_tag']
            self._config['ami'] = ami.get_by_tag(client, ami_tag)

    def set_az(self, az):
        self._config['az'] = az

    @property
    def ami_tag(self):
        return self._config['ami_tag']

    @property
    def type(self):
        return self._config['type']

    @property
    def max_bid(self):
        return float(self._config['max_bid'])

    @property
    def security_group_id(self):
        return self._config['security_group_id']

    @property
    def ami(self):
        return self._config['ami']

    @property
    def key_name(self):
        return self._config['key_name']

    @property
    def az(self):
        return self._config['az']

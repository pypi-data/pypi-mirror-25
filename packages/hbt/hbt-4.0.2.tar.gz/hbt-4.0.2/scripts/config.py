#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import expanduser, abspath, dirname, join
import os
import io
import json

import six

DEFAULT_CONFIG_LOCATION = expanduser("~/.hbtrc")

DEFAULT_CONFIG = {
    'jira_url': 'http://jira.56qq.cn',
    'reviewboard_url': 'http://reviewboard.56qq.com',
    'clean_check': True,
    'commit_message_check': True,
    'checkstyle': True,
    'hbt_dir': dirname(abspath(__file__)),
    'jira_user': '',
    'jira_password': ''
}


class InvalidConfigError(ValueError):
    """Raised if an invalid configuration is encountered."""

    def __init__(self, message):
        super(InvalidConfigError, self).__init__(message)


class HBTConfig(object):
    def __init__(self, filename=None):
        if filename is None and os.path.isfile(DEFAULT_CONFIG_LOCATION):
            filename = DEFAULT_CONFIG_LOCATION

        self.override(DEFAULT_CONFIG)
        if filename is not None:
            try:
                with io.open(filename, encoding='utf-8') as f:
                    file_config = json.loads(f.read())
            except ValueError as e:
                raise InvalidConfigError("Failed to read configuration file '{}'. Error: {}".format(filename, e))
            self.override(file_config)
            if not (self.jira_user and self.jira_password and self.hbt_dir):
                raise InvalidConfigError(u"jira_user, jira_password, hbt_dir不能为空")

    # noinspection PyCompatibility
    def make_unicode(self, config):
        if six.PY2:
            # Sometimes (depending on the source of the config value) an argument will be str instead of unicode
            # to unify that and ease further usage of the config, we convert everything to unicode
            for k, v in config.items():
                if type(v) is str:
                    config[k] = unicode(v, "utf-8")
        return config

    def override(self, config):
        # abs_path_config = self.make_unicode(self.make_paths_absolute(config, ["path", "response_log"]))
        self.__dict__.update(config)

    def make_paths_absolute(self, config, keys):
        abs_path_config = dict(config)
        for key in keys:
            if key in abs_path_config and abs_path_config[key] is not None and not os.path.isabs(abs_path_config[key]):
                abs_path_config[key] = join(os.getcwd(), abs_path_config[key])
        return abs_path_config


if __name__ == '__main__':
    c = HBTConfig()
    print c

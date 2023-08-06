#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import re
import time

from jira import JIRA, JIRAError
from rbtools.utils.commands import get_review_request
from rbtools.api.client import RBClient


class SourceFile(object):
    COPYRIGHT_TEMPLATE = '%s'

    TYPE_JAVA = 'java'
    TYPE_XML = 'xml'
    TYPE_OTHERS = 'others'

    LEVEL_ERROR = 'ERROR'
    LEVEL_WARN = 'WARN'

    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.abs_path = os.path.join(path, name)
        self.created = self.get_create_year()
        self.current = self.get_current_year()

    @staticmethod
    def create(path, name):
        if name.endswith(SourceFile.TYPE_JAVA):
            return JavaFile(path, name)
        elif name.endswith(SourceFile.TYPE_XML):
            return XmlFile(path, name)
        else:
            return None

    def check_style(self, command):
        return 0

    def get_level_count(self, lines, level):
        return len(re.compile(r"\[%s\]" % level).findall(lines))

    def add_copyright(self):
        print self.abs_path
        with open(self.abs_path) as f:
            lines = self.remove_leading_comment(f.readlines())

        with open(self.abs_path, 'w') as f:
            f.write(self.get_copyright_text())
            f.writelines(lines)

    def get_create_year(self):
        command = 'git log --follow --format=%ai --reverse -- {} | head -1'.format(self.abs_path)

        # output example: 2015-11-10 15:44:29 +0800
        date_format = subprocess.check_output(command, shell=True)

        if len(date_format) == 0:
            return self.get_current_year()

        return date_format.split('-')[0]

    def get_current_year(self):
        return time.strftime('%Y', time.localtime(time.time()))

    def remove_leading_comment(self, lines):
        idx = 0
        for idx, line in enumerate(lines):
            if self.BODY_PATTERN.match(line):
                break
        return lines[idx:]

    def get_copyright_text(self):
        return self.COPYRIGHT_TEMPLATE % \
               (self.current if self.created == self.current else
                '%s - %s' % (self.created, self.current))


class JavaFile(SourceFile):
    COPYRIGHT_TEMPLATE = """\
/*
 * Copyright (C) %s 贵阳货车帮科技有限公司
 */\n
"""
    BODY_PATTERN = re.compile(r'^package.+$')

    def check_style(self, command):
        result = subprocess.check_output(command + ' ' + self.abs_path, shell=True)
        return self.get_level_count(result, self.LEVEL_ERROR) + self.get_level_count(result, self.LEVEL_WARN)


class XmlFile(SourceFile):
    COPYRIGHT_TEMPLATE = """\
<?xml version="1.0" encoding="utf-8"?>
<!-- Copyright (C) %s 贵阳货车帮科技有限公司 -->\n"""
    BODY_PATTERN = re.compile(r'^<(!DOCTYPE|[a-zA-Z]).+$')


class WorkSpace(object):
    SUBJECT_PATTERN = r'^\s*(feat|fix|docs|style|refactor|chore)?\s*\((.*)\)\s*[:|：]\s*(.+)$'
    AFFECT_PATTERN = r'^[测试影响|影响]'
    REVIEW_REQUEST_PATTERN = r'^\s*%s/r/(\d+)/\s*$'
    RENAME_PATTERN = r'^\s*R\d+\s+.+[\.java|\.xml]\s+(.+[\.java|\.xml])\s*$'
    ADD_OR_MODIFY_PATTERN = r'^\s*[M|A]\s+(.+[\.java|\.xml])\s*$'

    GROUP_INDEX_FILE_NAME = 1

    STATUS_SUBMITTED = 'submitted'

    def __init__(self, config):
        self.config = config
        self.issue_id = None
        self.commit_message = subprocess.check_output('git log --format=%B -n 1', shell=True).strip().split('\n')
        self.review_url, self.request_id = self.get_review_url()

    def is_clean(self):
        return self.config.clean_check and '' != subprocess.check_output('git status --porcelain --untracked-files=no', shell=True)

    def get_review_url(self):
        pattern = re.compile(self.REVIEW_REQUEST_PATTERN % self.config.reviewboard_url)
        for line in self.commit_message:
            result = pattern.match(line)
            if result:
                return line, result.group(1)
        else:
            print '[WARN]: 没有解析到reviewboard url'
            return None, None

    def check_commit_message(self):
        if not self.config.commit_message_check:
            return ''

        if not self.commit_message:
            return u'commit message为空'

        result = self.check_subject(self.commit_message[0])
        if result:
            return result

        if not self.config.strict:
            # 非严格模式，不检查body和测试影响
            return ''

        result = self.check_affect(self.commit_message)
        if result:
            return result

        result, reason = self.check_body(self.commit_message[1:-1])
        if not result:
            return False, reason

        return True, ''

    def check_subject(self, subject):
        result = re.compile(self.SUBJECT_PATTERN).match(subject)
        reason = u'第一行为subject,格式为 <type>(<issue_id>): <subject>'
        if result:
            self.issue_id = result.group(2)
            reason = ''
        return reason

    def check_body(self, lines):
        if len(lines) < 3:
            return False, u"commit message缺少<subject>, <body>, <affect>元素之一"
        if len(lines) > 1 and lines[1].strip():
            return False, u"标题的下面应该为空行"

        if lines[-2].strip():
            return False, u'"测试影响"与body之间需要空行'
        if lines[1].strip():
            return False, u'subject与body之间需要空行'
        return True, ''

    def check_affect(self, lines):
        pattern = re.compile(self.AFFECT_PATTERN)
        for idx, line in enumerate(lines):
            if pattern.match(line):
                break
        else:
            return u'没有"测试影响"描述'

        if lines[idx - 1].strip():
            return u'"测试影响"与body之间需要空行'
        if idx < 4:
            return u'缺少<body>'

        return ''

    def get_commit_message(self):
        self.commit_message = subprocess.check_output('git log --format=%B -n 1', shell=True).strip().split('\n')
        return self.commit_message

    def check_land_request(self):
        if not self.request_id:
            return u'未能查询到review request id'

        print u'开始检查review request是否能够提交： ' + self.request_id
        review_request = self.get_review_request_by_id()

        if not review_request.approved:
            return review_request.approval_failure
        return ''

    def get_review_request_by_id(self):
        client = RBClient(self.config.reviewboard_url)
        return get_review_request(self.request_id, client.get_root())

    def exist_remote_branch(self, name):
        lines = subprocess.check_output('git branch -a', shell=True).split('\n')
        remote_name = 'remotes/origin/{}'.format(name)

        for line in lines:
            if line.strip() == remote_name:
                return True
        else:
            return False

    def push_change(self, branch_name):
        return subprocess.call('git push origin HEAD:' + branch_name, shell=True)

    def update_jira_comment(self):
        jira_user = subprocess.check_output('git config jira.user', shell=True).strip() or self.config.user
        jira_password = subprocess.check_output('git config jira.pwd', shell=True).strip() or self.config.password

        authed_jira = JIRA(server=(self.config.jira_url), basic_auth=(jira_user, jira_password))
        if not self.issue_id:
            return False
        issue = authed_jira.issue(self.issue_id)
        authed_jira.add_comment(issue, '\n'.join(self.commit_message))

        # '4' 代表状态是 开发中
        try:
            authed_jira.transition_issue(issue, transition='4')
        except JIRAError:
            # 当jira状态已经为“开发中”时，这里transition会抛异常。ignore it
            return False
        return True

    def close_review_request(self):
        commit_id = subprocess.check_output('git log --format="%H" -n 1', shell=True)
        description = 'hbt closed: {}'.format(commit_id)

        review_request = self.get_review_request_by_id(self.request_id)
        if review_request.status == self.STATUS_SUBMITTED:
            print 'Review request {} is already submitted.'.format(self.request_id)
            return

        review_request.update(status=self.STATUS_SUBMITTED, description=description)

    def get_commit_file_list(self, lines):
        files = list()
        rename_pattern = re.compile(self.RENAME_PATTERN)
        update_pattern = re.compile(self.ADD_OR_MODIFY_PATTERN)
        for line in lines:
            result = rename_pattern.match(line)
            if result:
                files.append(result.group(self.GROUP_INDEX_FILE_NAME))
                continue

            result = update_pattern.match(line)
            if result:
                files.append(result.group(self.GROUP_INDEX_FILE_NAME))

        return files

    def committed_files(self):
        commit_log = subprocess.check_output('git log --name-status --pretty=format:"" -n 1', shell=True)
        # files = self.get_commit_file_list(commit_log.split('\n'))
        return [SourceFile.create(os.path.dirname(f), os.path.basename(f)) for f in self.get_commit_file_list(commit_log.split('\n'))]

    def ammend_message(self):
        subprocess.call('git commit -a --amend --no-edit', shell=True)


if __name__ == '__main__':
    java = SourceFile.create('.', 'TestNoWarn.java')
    print java.path, java.name
    java.add_copyright()

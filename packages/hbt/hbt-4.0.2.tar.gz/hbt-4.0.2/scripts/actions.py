#!/usr/bin/env python
# -*- coding: utf-8 -*-
from jira import JIRA, JIRAError
from rbtools.utils.commands import get_review_request
from rbtools.api.client import RBClient
import subprocess
import re
import os
import platform
from sourcefile import SourceFile


SUCCESS = ''


class Action(object):
    subject_re = r'^\s*(feat|fix|docs|style|refactor|chore)?\s*\((.*)\)\s*[:|：]\s*(.+)\n'
    new_line_re = r'\n'
    body_re = r'((?:.+\n)+)'
    affect_re = r'^([测试影响|影响].*)'
    commit_re = subject_re + new_line_re + body_re + new_line_re + affect_re

    rename_re = r'^\s*R\d+\s+.+[\.java|\.xml]\s+(.+[\.java|\.xml])\s*$'
    update_re = r'^\s*[M|A]\s+(.+[\.java|\.xml])\s*$'

    GROUP_INDEX_FILE_NAME = 1

    STATUS_SUBMITTED = 'submitted'

    def __init__(self, config, ctx, commit_message=''):
        self.config = config
        self.context = ctx
        self.commit_message = commit_message or subprocess.check_output('git log --format=%B -n 1', shell=True).strip()

    def get_issue_id(self):
        return re.compile(self.subject_re).match(self.commit_message).group(2)

    def get_review_request_by_id(self, request_id):
        client = RBClient(self.config.reviewboard_url)
        return get_review_request(request_id, client.get_root())

    def get_review_url(self, lines=None):
        if not lines:
            lines = self.commit_message.split('\n')
        review_request_pattern = re.compile(r'^\s*%s/r/(\d+)/\s*$' % self.config.reviewboard_url)
        for line in lines:
            result = review_request_pattern.match(line)
            if result:
                return line, result.group(1)
        else:
            print u'[WARN]: 没有解析到reviewboard url'
            return None, None

    def get_committed(self):
        commit_log = subprocess.check_output('git log --name-status --pretty=format:"" -n 1', shell=True)
        return [SourceFile.create(os.path.dirname(f), os.path.basename(f)) for f in
                self.get_commit_file_list(commit_log.split('\n'))]

    def get_commit_file_list(self, lines):
        files = list()
        rename_pattern = re.compile(self.rename_re)
        update_pattern = re.compile(self.update_re)
        for line in lines:
            result = rename_pattern.match(line)
            if result:
                files.append(result.group(self.GROUP_INDEX_FILE_NAME))
                continue

            result = update_pattern.match(line)
            if result:
                files.append(result.group(self.GROUP_INDEX_FILE_NAME))

        return files


class WorkspaceCleanAction(Action):
    def do(self):
        if self.config.clean_check and \
                '' != subprocess.check_output('git status --porcelain --untracked-files=no', shell=True):
            return u'WARNING: 有未commit的文件。请commit后再发送review request'
        return SUCCESS


class CommitCheckAction(Action):
    def do(self):
        if not self.config.commit_message_check:
            return ''

        if not self.commit_message:
            return u'commit message为空'

        return SUCCESS if re.compile(self.commit_re, re.MULTILINE).match(self.commit_message) else u'commit message格式不符合要求'


class LandCheckAction(Action):
    def do(self):
        review_url, request_id = self.get_review_url()
        if not request_id:
            return u'未能查询到review request id'

        print u'开始检查review request是否能够提交： ' + request_id
        review_request = self.get_review_request_by_id(request_id)

        if not review_request.approved:
            print review_request.approval_failure
            return u'reviewboard检查失败'

        if not self.exist_remote_branch():
            return u'不存在的远程分支。请检查分支名。'

        return SUCCESS

    def exist_remote_branch(self):
        remote_name = 'remotes/origin/{}'.format(self.context.params['branch'])

        for line in subprocess.check_output('git branch -a', shell=True).split('\n'):
            if line.strip() == remote_name:
                return True
        else:
            return False


class PushAction(Action):
    def do(self):
        return SUCCESS if subprocess.call('git push origin HEAD:' + self.context.params['branch'], shell=True) == 0 \
                       else u'push失败'


class JiraUpdateAction(Action):
    def do(self):
        authed_jira = JIRA(server=self.config.jira_url, basic_auth=(self.config.jira_user, self.config.jira_password))
        issue = authed_jira.issue(self.get_issue_id())
        authed_jira.add_comment(issue, self.commit_message)

        # '4' 代表状态是 开发中
        try:
            authed_jira.transition_issue(issue, transition='4')
        except JIRAError:
            # 当jira状态已经为“开发中”时，这里transition会抛异常。ignore it
            pass
        return SUCCESS


class CloseReviewboardAction(Action):
    def do(self):
        commit_id = subprocess.check_output('git log --format="%H" -n 1', shell=True)
        description = 'hbt closed: {}'.format(commit_id)

        _, request_id = self.get_review_url()
        if not request_id:
            return u'未能查询到review request id'

        review_request = self.get_review_request_by_id(request_id)
        if review_request.status == self.STATUS_SUBMITTED:
            return u'Review request {} is already submitted.'.format(request_id)

        review_request.update(status=self.STATUS_SUBMITTED, description=description)
        return SUCCESS


class CopyrightUpdateAction(Action):
    def do(self):
        for f in self.get_committed():
            f.add_copyright()
        return SUCCESS


class AmendMessageAction(Action):
    def do(self):
        return SUCCESS if subprocess.call('git commit -a --amend --no-edit', shell=True) == 0 else \
               u'更新commit message失败'


class StyleCheckAction(Action):
    CYGWIN_SYSTEM_PREFIX = 'CYGWIN'
    CHECKSTYLE_JAR_FILE_NAME = 'checkstyle-all.jar'
    CHECKSTYLE_CONFIG_FILE_NAME = 'checkstyle-config.xml'

    def do(self):
        return SUCCESS if self.config.checkstyle or self.style_errors() == 0 else\
            '\nWARNING: You must fix the errors and warnings first, then post review again'

    def style_errors(self):
        hbt_dir = self.config.hbt_dir
        if platform.system().startswith(self.CYGWIN_SYSTEM_PREFIX):
            # change to cygwin path
            hbt_dir = subprocess.check_output('cygpath -m "' + self.config.hbt_dir + '"', shell=True).strip()

        jar_file = os.path.join(hbt_dir, self.CHECKSTYLE_JAR_FILE_NAME)
        config_file = os.path.join(hbt_dir, self.CHECKSTYLE_CONFIG_FILE_NAME)

        # check code command
        command = 'java -jar ' + jar_file + ' -c ' + config_file

        for f in self.get_committed():
            if f.check_style(command) != 0:
                return 1
        return 0


class RBTAction(Action):
    review_request_re = r'^\s*%s/r/(\d+)/\s*$'

    CHECKSTYLE_TAG = '[checked_4_0_2]'

    def do(self):
        rbt_command = 'rbt %s %s' % (self.context.info_name.encode('ascii', 'ignore'), ' '.join(arg for arg in self.context.params['rbt_args']))
        summary =  self.commit_message.split('\n')[0].replace('"', '\\\"')
        if summary:
            rbt_command += ' --summary "%s %s"' % (self.CHECKSTYLE_TAG, summary)
        post_message = subprocess.check_output(rbt_command, shell=True)

        review_url, request_id = self.get_review_url(post_message.split('\n'))
        if not review_url:
            return

        new_message = self.update_commit_message(review_url).replace('"', '\\\"')
        # update review board url to commit message
        subprocess.call('git commit --amend -m "%s"' % new_message, shell=True)
        return SUCCESS

    def update_commit_message(self, review_url):
        lines = []
        has_updated = False

        for line in self.commit_message.split('\n'):
            if re.compile(self.review_request_re % self.config.reviewboard_url).match(line):
                lines.append(review_url)
                has_updated = True
            else:
                lines.append(line)

        if not has_updated:
            lines.append(review_url)
            lines.append('%s/browse/%s' % (self.config.jira_url, self.get_issue_id()))
        return '\n'.join(lines)

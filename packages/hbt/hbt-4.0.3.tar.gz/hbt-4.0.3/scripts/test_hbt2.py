#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest
from config import HBTConfig
from actions import CommitCheckAction, Action
from sourcefile import SourceFile, JavaFile, XmlFile

JAVA_CONTENT = """\
package com.wlqq.data.net;

import com.raizlabs.android.dbflow.annotation.NotNull;
import com.wlqq.data.request.LoginParams;
import com.wlqq.login.model.Session;

import java.util.Map;

import io.reactivex.Observable;

/**
 * Interfaces of gas station.
 */
public interface IGasApi {
    /**
     * Get an {@link Observable} which will emit a {@link Session}.
     */
    Observable<Session> login(@NotNull Map<String, String> headers, @NotNull LoginParams params);
    void logout();
}
"""

XML_CONTENT = """\
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright (C) 2017 贵阳货车帮科技有限公司 -->
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">

<mapper namespace="com.wlqq.dms.api.build.dao.BuildLogPatternDao">
    <sql id="column">
        uuid,
        pattern,
        error_code AS errorCode,
        error_message AS errorMessage,
        create_user AS createUser,
		create_time AS createTime,
		update_user AS updateUser,
		update_time AS updateTime
    </sql>

    <select id="list" resultType="com.wlqq.dms.api.build.domain.BuildLogPattern">
        SELECT * from dms_build_log_pattern
    </select>
</mapper>
"""


def split_file_path(p):
    return [os.path.dirname(p), os.path.basename(p)]

class Hbt2TestCase(unittest.TestCase):
    java_file_path = 'TestJava.java'
    xml_file_path = 'testXml.xml'

    def setUp(self):
        with open(self.java_file_path, 'w') as f:
            f.write(JAVA_CONTENT)
        with open(self.xml_file_path, 'w') as f:
            f.write(XML_CONTENT)

    def tearDown(self):
        for p in [self.java_file_path, self.xml_file_path]:
            if os.path.exists(p):
                os.remove(p)

    def test_config(self):
        default_config = HBTConfig('hbtrc')

        self.assertEqual(default_config.jira_url, "http://jira.56qq.cn")
        self.assertEqual(default_config.reviewboard_url, "http://reviewboard.56qq.com")
        self.assertEqual(default_config.clean_check, True)
        self.assertEqual(default_config.commit_message_check, True)
        self.assertEqual(default_config.checkstyle, True)
        self.assertEqual(default_config.jira_user, "user")
        self.assertEqual(default_config.jira_password, "password")
        self.assertEqual(default_config.hbt_dir, "/a/b/c")

    def test_sourcefile_op(self):
        sf = SourceFile.create(*split_file_path(self.java_file_path))
        self.assertTrue(isinstance(sf, JavaFile))
        sf.add_copyright()

        with open(self.java_file_path) as f:
            content = f.read()
            self.assertTrue(content.startswith(sf.get_copyright_text()))

        sf = SourceFile.create(*split_file_path(self.xml_file_path))
        self.assertTrue(isinstance(sf, XmlFile))
        sf.add_copyright()

        with open(self.xml_file_path) as f:
            content = f.read()
            self.assertTrue(content.startswith(sf.get_copyright_text()))

    def test_commit_message(self):
        config = HBTConfig('hbtrc')
        config.commit_message_check = True

        valid_messages = [
            """\
fix(ANDROID_INFRA-57): summary

body

测试影响\
""",
            """\
fix(ANDROID_INFRA-57): summary

body

影响：启动页面

http://reviewboard.56qq.com/r/3889/
http://jira.56qq.cn/browse/ANDROID_INFRA-96\
""",
            """\
fix(ANDROID_INFRA-57): summary

body

测试影响
""",
            """\
feat(ANDROID_INFRA-57): summary

body

测试影响
            """,
            """\
docs(ANDROID_INFRA-57): summary

body

测试影响
""",
        ]
        action = CommitCheckAction(config, None)
        for msg in valid_messages:
            action.commit_message = msg
            self.assertFalse(action.do())

        invalid_messages = [
            """\
unknownfeat(ANDROID_INFRA-57): summary

body

测试影响
                        """,
            """\
unknownfeat(ANDROID_INFRA-57): summary

测试影响
                        """,
            """\
unknownfeat(ANDROID_INFRA-57): summary
测试影响
                        """,
            """\
unknownfeat(ANDROID_INFRA-57): summary

测试影响
                                    """,
            """\
unknownfeat(ANDROID_INFRA-57): summary

这里是正文
            """,
            """\
这里是正文

测试影响
            """,
            """\
feat ANDROID_INFRA-57 summary

测试影响
            """
    ]
        for msg in invalid_messages:
            action.commit_message = msg
            self.assertTrue(action.do())

    def test_review_url(self):
        config = HBTConfig('hbtrc')
        request_id = '3889'
        review_url = 'http://reviewboard.56qq.com/r/%s/' % request_id
        commit_message = """\
fix(ANDROID_INFRA-57): summary

body

影响：启动页面

http://reviewboard.56qq.com/r/3889/
http://jira.56qq.cn/browse/ANDROID_INFRA-96
        """
        action = Action(config, None, commit_message)
        self.assertEqual((review_url, request_id), action.get_review_url())

        commit_message = """\
        fix(ANDROID_INFRA-57): summary

        body

        影响：启动页面
                """
        action = Action(config, None, commit_message)
        self.assertEqual((None, None), action.get_review_url())

    def test_commit_file_list(self):
        commit_javas = """\
M   src/main/java/com/wlqq/checkout/CheckOutActivity.java
D   src/main/java/com/wlqq/shift/activity/FixShiftSuccessActivity.java
A   src/main/java/com/wlqq/shift/activity/UnConfirmedShiftActivity.java
M   src/main/res/values/values.xml
D   src/main/res/values/colors.xml
A   src/main/res/values/strings.xml
R100    debug.java  test.java
R109    src.xml  dest.xml
            """
        self.assertEqual(6, len(Action(None, None, None).get_commit_file_list(commit_javas.split('\n'))))

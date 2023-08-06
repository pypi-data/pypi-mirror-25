#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest
import config
from sourcefile import SourceFile, JavaFile

JAVA_CONTENT = """
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


class Hbt2TestCase(unittest.TestCase):
    java_file_path = 'TestJava.java'

    def setUp(self):
        with open(self.java_file_path, 'w') as f:
            f.write(JAVA_CONTENT)

    def tearDown(self):
        if os.path.exists(self.java_file_path):
            os.remove(self.java_file_path)

    def test_config(self):
        default_config = config.HBTConfig('hbtrc')

        self.assertEqual(default_config.jira_url, "http://jira.56qq.cn")
        self.assertEqual(default_config.reviewboard_url, "http://reviewboard.56qq.com")
        self.assertEqual(default_config.clean_check, True)
        self.assertEqual(default_config.commit_message_check, True)
        self.assertEqual(default_config.checkstyle, True)
        self.assertEqual(default_config.jira_user, "user")
        self.assertEqual(default_config.jira_password, "password")
        self.assertEqual(default_config.hbt_dir, "/a/b/c")

    def test_sourcefile_op(self):
        sf = SourceFile.create(*self.split_file_path(self.java_file_path))
        self.assertTrue(isinstance(sf, JavaFile))
        sf.add_copyright()

        with open(self.java_file_path) as f:
            content = f.read()
            self.assertTrue(content.startswith(sf.get_copyright_text()))

    def split_file_path(self, p):
        return [os.path.dirname(p), os.path.basename(p)]

# coding=utf-8

from __future__ import unicode_literals

import unittest

from faker import Factory

from tests import string_types

class TestJob(unittest.TestCase):
    """
    Test Job
    """

    def setUp(self):
        self.factory = Factory.create()

    def test_job(self):
        job = self.factory.job()
        assert isinstance(job, string_types)

class TestKoKR(unittest.TestCase):
    """
    Test Job ko_KR
    """

    def setUp(self):
        self.factory = Factory.create('ko_KR')

    def test_job(self):
        job = self.factory.job()
        assert isinstance(job, string_types)

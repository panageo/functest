#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import mock
import unittest

from functest.core import vnf_base
from functest.core import testcase_base


class VnfBaseTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def setUp(self):
        self.test = vnf_base.VnfOnBoardingBase(project='functest',
                                               case='aaa')
        self.test.project = "functest"
        self.test.case_name = "aaa"
        self.test.start_time = "1"
        self.test.stop_time = "5"
        self.test.criteria = ""
        self.test.details = {"orchestrator": {"status": "PASS",
                                              "result": "",
                                              "duration": 20},
                             "vnf": {"status": "PASS",
                                     "result": "",
                                     "duration": 15},
                             "test_vnf": {"status": "FAIL",
                                          "result": "",
                                          "duration": 5}}

    @mock.patch('logging.Logger.error')
    def test_deploy_vnf_unimplemented(self, mock):
        self.assertEqual(self.test.deploy_vnf(),
                         testcase_base.TestcaseBase.EX_TESTCASE_FAILED)
        mock.assert_called_with('VNF must be deployed')

    @mock.patch('logging.Logger.error')
    def test_test_vnf_unimplemented(self, mock):
        self.assertEqual(self.test.test_vnf(),
                         testcase_base.TestcaseBase.EX_TESTCASE_FAILED)
        mock.assert_called_with('VNF must be tested')

    def test_parse_results(self):
        self.assertNotEqual(self.test.parse_results(), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)

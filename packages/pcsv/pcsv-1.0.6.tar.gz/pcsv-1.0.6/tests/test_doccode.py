# test_doccode.py
# Copyright (c) 2013-2017 Pablo Acosta-Serafini
# See LICENSE for details
# pylint: disable=C0111,C0302,E1129,R0914,R0915,W0212,W0640

# Standard library imports
from __future__ import print_function
import os
import subprocess


###
# Functions
###
def test_pcsv_doccode():
    """ Test code used in pcsv module """
    script_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '..', 'docs', 'support'
    )
    for num in range(1, 7):
        script_name = os.path.join(
            script_dir, 'pcsv_example_{0}.py'.format(num))
        proc = subprocess.Popen(
            ['python', script_name], stdout=subprocess.PIPE
        )
        stdout, stderr = proc.communicate()
        if proc.returncode != 0:
            print('Script: {0}'.format(script_name))
            print('STDOUT: {0}'.format(stdout))
            print('STDERR: {0}'.format(stderr))
        assert proc.returncode == 0

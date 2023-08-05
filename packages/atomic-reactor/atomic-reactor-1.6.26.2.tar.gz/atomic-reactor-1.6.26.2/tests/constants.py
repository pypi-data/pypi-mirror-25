# -*- coding: utf-8 -*-
"""
Copyright (c) 2015 Red Hat, Inc
All rights reserved.

This software may be modified and distributed under the terms
of the BSD license. See the LICENSE file for details.
"""

from __future__ import unicode_literals

import os

HERE = os.path.dirname(__file__)
FILES = os.path.join(HERE, 'files')

MOCK = os.environ.get('NOMOCK') is None

INPUT_IMAGE = "busybox:latest"
DOCKERFILE_FILENAME = 'Dockerfile'
DOCKERFILE_GIT = "https://github.com/TomasTomecek/docker-hello-world.git"
DOCKERFILE_SHA1 = "6e592f1420efcd331cd28b360a7e02f669caf540"
DOCKERFILE_OK_PATH = os.path.join(FILES, 'docker-hello-world')
DOCKERFILE_ERROR_BUILD_PATH = os.path.join(FILES, 'docker-hello-world-error-build')
DOCKERFILE_SUBDIR_PATH = os.path.join(FILES, 'df-in-subdir')

SOURCE = {
    'provider': 'git',
    'uri': DOCKERFILE_GIT,
    'provider_params': {
        'git_commit': 'master',
    }
}

MOCK_SOURCE = {'provider': 'git', 'uri': 'asd'}

REGISTRY_PORT = "5000"
DOCKER0_IP = "172.17.42.1"
TEST_IMAGE = "atomic-reactor-test-image"

LOCALHOST_REGISTRY = "localhost:%s" % REGISTRY_PORT
DOCKER0_REGISTRY = "%s:%s" % (DOCKER0_IP, REGISTRY_PORT)
LOCALHOST_REGISTRY_HTTP = "http://%s" % LOCALHOST_REGISTRY
DOCKER0_REGISTRY_HTTP = "http://%s" % DOCKER0_REGISTRY

COMMAND = "eporeporjgpeorjgpeorjgpeorjgpeorjgpeorjg"

IMPORTED_IMAGE_ID = 'eee28534d167d7b3297eace1fc32c46aabedc40696e48ae04c7654f974700cc2'

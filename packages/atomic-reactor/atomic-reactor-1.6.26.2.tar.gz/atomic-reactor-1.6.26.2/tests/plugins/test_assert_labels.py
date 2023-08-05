"""
Copyright (c) 2015 Red Hat, Inc
All rights reserved.

This software may be modified and distributed under the terms
of the BSD license. See the LICENSE file for details.
"""

from __future__ import unicode_literals

import pytest
from atomic_reactor.inner import DockerBuildWorkflow
from atomic_reactor.plugin import PreBuildPluginsRunner, PluginFailedException
from atomic_reactor.plugins.pre_assert_labels import AssertLabelsPlugin
from atomic_reactor.util import ImageName, df_parser
from tests.constants import MOCK_SOURCE
from tests.fixtures import docker_tasker  # noqa


class Y(object):
    pass


class X(object):
    image_id = "xxx"
    source = Y()
    source.dockerfile_path = None
    source.path = None
    base_image = ImageName(repo="qwe", tag="asd")


DF_CONTENT = """
FROM fedora
RUN yum install -y python-django
CMD blabla"""
DF_CONTENT_LABELS = DF_CONTENT+'\nLABEL "name"="rainbow" "version"="123" "release"="1"'

@pytest.mark.parametrize('df_content, req_labels, expected', [  # noqa
    (DF_CONTENT, None, PluginFailedException()),
    (DF_CONTENT_LABELS, None, None),
    (DF_CONTENT_LABELS, ['xyz'], PluginFailedException())
])
def test_assertlabels_plugin(tmpdir, docker_tasker, df_content, req_labels, expected):
    df = df_parser(str(tmpdir))
    df.content = df_content

    workflow = DockerBuildWorkflow(MOCK_SOURCE, 'test-image')
    workflow.builder = X
    workflow.builder.df_path = df.dockerfile_path
    workflow.builder.df_dir = str(tmpdir)

    runner = PreBuildPluginsRunner(
        docker_tasker,
        workflow,
        [{
            'name': AssertLabelsPlugin.key,
            'args': {'required_labels': req_labels}
        }]
    )

    assert AssertLabelsPlugin.key is not None

    if isinstance(expected, PluginFailedException):
        with pytest.raises(PluginFailedException):
            runner.run()
    else:
        runner.run()


@pytest.mark.parametrize('df_content, req_labels', [  # noqa
    (DF_CONTENT_LABELS, ['xyz']),
    (DF_CONTENT_LABELS, ['xyz', 'abc']),
    (DF_CONTENT_LABELS, ['xyz', 'some', 'some2'])
])
def test_all_missing_required_labels(tmpdir, docker_tasker, caplog, df_content, req_labels):
    df = df_parser(str(tmpdir))
    df.content = df_content

    workflow = DockerBuildWorkflow(MOCK_SOURCE, 'test-image')
    workflow.builder = X
    workflow.builder.df_path = df.dockerfile_path
    workflow.builder.df_dir = str(tmpdir)

    runner = PreBuildPluginsRunner(
        docker_tasker,
        workflow,
        [{
            'name': AssertLabelsPlugin.key,
            'args': {'required_labels': req_labels}
        }]
    )

    assert AssertLabelsPlugin.key is not None

    with pytest.raises(PluginFailedException):
        runner.run()

    error_msg = "Dockerfile is missing required labels: {0}".format(req_labels)
    assert error_msg in caplog.text()

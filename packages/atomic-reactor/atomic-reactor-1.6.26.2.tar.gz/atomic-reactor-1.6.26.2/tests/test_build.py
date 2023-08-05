"""
Copyright (c) 2015 Red Hat, Inc
All rights reserved.

This software may be modified and distributed under the terms
of the BSD license. See the LICENSE file for details.
"""
from __future__ import unicode_literals

import pytest

from atomic_reactor.build import InsideBuilder, BuildResult
from atomic_reactor.core import DockerTasker  # noqa
from atomic_reactor.source import get_source_instance_for
from atomic_reactor.util import ImageName
from tests.constants import LOCALHOST_REGISTRY, DOCKERFILE_OK_PATH, MOCK, SOURCE
from tests.util import requires_internet
from flexmock import flexmock

if MOCK:
    from tests.docker_mock import mock_docker

# This stuff is used in tests; you have to have internet connection,
# running registry on port 5000 and it helps if you've pulled fedora:latest before
git_base_repo = "fedora"
git_base_tag = "latest"
git_base_image = ImageName(registry=LOCALHOST_REGISTRY, repo="fedora", tag="latest")


with_all_sources = pytest.mark.parametrize('source_params', [
    SOURCE,
    {'provider': 'path', 'uri': 'file://' + DOCKERFILE_OK_PATH}
])


@requires_internet
@with_all_sources
def test_inspect_built_image(tmpdir, source_params):
    provided_image = "test-build:test_tag"
    if MOCK:
        mock_docker(provided_image_repotags=provided_image)

    flexmock(InsideBuilder, ensure_is_built=None)
    source_params.update({'tmpdir': str(tmpdir)})
    s = get_source_instance_for(source_params)
    b = InsideBuilder(s, provided_image)
    built_inspect = b.inspect_built_image()

    assert built_inspect is not None
    assert built_inspect["Id"] is not None


@requires_internet
@with_all_sources
def test_inspect_base_image(tmpdir, source_params):
    if MOCK:
        mock_docker()

    source_params.update({'tmpdir': str(tmpdir)})
    s = get_source_instance_for(source_params)
    b = InsideBuilder(s, '')
    built_inspect = b.inspect_base_image()

    assert built_inspect is not None
    assert built_inspect["Id"] is not None


@requires_internet
@with_all_sources
@pytest.mark.parametrize(('image', 'will_raise'), [
    (
        "buildroot-fedora:latest",
        False,
    ),
    (
        "non-existing",
        True,
    ),
])
def test_get_base_image_info(tmpdir, source_params, image, will_raise):
    if MOCK:
        mock_docker(provided_image_repotags=image)

    source_params.update({'tmpdir': str(tmpdir)})
    s = get_source_instance_for(source_params)
    b = InsideBuilder(s, image)

    if will_raise:
        with pytest.raises(Exception):
            built_inspect = b.get_base_image_info()
    else:
        built_inspect = b.get_base_image_info()
        assert built_inspect is not None
        assert built_inspect["Id"] is not None
        assert built_inspect["RepoTags"] is not None


@requires_internet
@with_all_sources
@pytest.mark.parametrize('is_built', [
    True,
    False,
])
def test_ensure_built(tmpdir, source_params, is_built):
    if MOCK:
        mock_docker()

    source_params.update({'tmpdir': str(tmpdir)})
    s = get_source_instance_for(source_params)
    b = InsideBuilder(s, '')
    b.is_built = is_built

    if is_built:
        assert b.ensure_is_built() is None
        with pytest.raises(Exception):
            b.ensure_not_built()
    else:
        assert b.ensure_not_built() is None
        with pytest.raises(Exception):
            b.ensure_is_built()


@requires_internet
@with_all_sources
@pytest.mark.parametrize(('image', 'will_raise'), [
    (
        "buildroot-fedora:latest",
        False,
    ),
    (
        "non-existing",
        True,
    ),
])
def test_get_image_built_info(tmpdir, source_params, image, will_raise):
    if MOCK:
        mock_docker(provided_image_repotags=image)

    source_params.update({'tmpdir': str(tmpdir)})
    s = get_source_instance_for(source_params)
    b = InsideBuilder(s, image)

    if will_raise:
        with pytest.raises(Exception):
            b.get_built_image_info()
    else:
        b.get_built_image_info()


def test_build_result():
    with pytest.raises(AssertionError):
        BuildResult(fail_reason='it happens', image_id='spam')

    with pytest.raises(AssertionError):
        BuildResult(fail_reason='', image_id='spam')

    assert BuildResult(fail_reason='it happens').is_failed()
    assert not BuildResult(image_id='spam').is_failed()

    assert BuildResult(image_id='spam', logs=list('logs')).logs == list('logs')

    assert BuildResult(fail_reason='it happens').fail_reason == 'it happens'
    assert BuildResult(image_id='spam').image_id == 'spam'

    assert BuildResult(image_id='spam', annotations={'ham': 'mah'}).annotations == {'ham': 'mah'}

    assert BuildResult(image_id='spam', labels={'ham': 'mah'}).labels == {'ham': 'mah'}

    assert BuildResult(image_id='spam').is_image_available()
    assert not BuildResult(fail_reason='it happens').is_image_available()
    assert not BuildResult.make_remote_image_result().is_image_available()

    assert not BuildResult.make_remote_image_result().is_failed()

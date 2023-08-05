"""
Copyright (c) 2016 Red Hat, Inc
All rights reserved.

This software may be modified and distributed under the terms
of the BSD license. See the LICENSE file for details.
"""

from __future__ import print_function


from collections import namedtuple
import koji
import logging
import os
import time

from atomic_reactor.constants import DEFAULT_DOWNLOAD_BLOCK_SIZE


logger = logging.getLogger(__name__)
Output = namedtuple('Output', ['file', 'metadata'])


class KojiUploadLogger(object):
    def __init__(self, logger, notable_percent=10):
        self.logger = logger
        self.notable_percent = notable_percent
        self.last_percent_done = 0

    def callback(self, offset, totalsize, size, t1, t2):  # pylint: disable=W0613
        if offset == 0:
            self.logger.debug("upload size: %.1fMiB", totalsize / 1024.0 / 1024)

        if not totalsize or not t1:
            return

        percent_done = 100 * offset / totalsize
        if (percent_done >= 99 or
                percent_done - self.last_percent_done >= self.notable_percent):
            self.last_percent_done = percent_done
            self.logger.debug("upload: %d%% done (%.1f MiB/sec)",
                              percent_done, size / t1 / 1024 / 1024)


def koji_login(session,
               proxyuser=None,
               ssl_certs_dir=None,
               krb_principal=None,
               krb_keytab=None):
    """
    Choose the correct login method based on the available credentials,
    and call that method on the provided session object.

    :param session: koji.ClientSession instance
    :param proxyuser: str, proxy user
    :param ssl_certs_dir: str, path to "cert", "ca", and "serverca"
    :param krb_principal: str, name of Kerberos principal
    :param krb_keytab: str, Kerberos keytab
    :return: None
    """

    kwargs = {}
    if proxyuser:
        kwargs['proxyuser'] = proxyuser

    if ssl_certs_dir:
        # Use certificates
        logger.info("Using SSL certificates for Koji authentication")
        result = session.ssl_login(os.path.join(ssl_certs_dir, 'cert'),
                                   os.path.join(ssl_certs_dir, 'ca'),
                                   os.path.join(ssl_certs_dir, 'serverca'),
                                   **kwargs)
    else:
        # Use Kerberos
        logger.info("Using Kerberos for Koji authentication")
        if krb_principal and krb_keytab:
            kwargs['principal'] = krb_principal
            kwargs['keytab'] = krb_keytab

        result = session.krb_login(**kwargs)

    if not result:
        raise RuntimeError('Unable to perform Koji authentication')

    return result


def create_koji_session(hub_url, auth_info=None):
    """
    Creates and returns a Koji session. If auth_info
    is provided, the session will be authenticated.

    :param hub_url: str, Koji hub URL
    :param auth_info: dict, authentication parameters used for koji_login
    :return: koji.ClientSession instance
    """
    session = koji.ClientSession(hub_url, opts={'krb_rdns': False})

    if auth_info is not None:
        koji_login(session, **auth_info)

    return session


class TaskWatcher(object):
    def __init__(self, session, task_id, poll_interval=5):
        self.session = session
        self.task_id = task_id
        self.poll_interval = poll_interval
        self.state = 'CANCELED'

    def wait(self):
        logger.debug("waiting for koji task %r to finish", self.task_id)
        while not self.session.taskFinished(self.task_id):
            time.sleep(self.poll_interval)

        logger.debug("koji task is finished, getting info")
        task_info = self.session.getTaskInfo(self.task_id, request=True)
        self.state = koji.TASK_STATES[task_info['state']]
        return self.state

    def failed(self):
        return self.state in ['CANCELED', 'FAILED']


def stream_task_output(session, task_id, file_name,
                       blocksize=DEFAULT_DOWNLOAD_BLOCK_SIZE):
    """
    Generator to download file from task without loading the whole
    file into memory.
    """
    logger.debug('Streaming {} from task {}'.format(file_name, task_id))
    offset = 0
    contents = '[PLACEHOLDER]'
    while contents:
        contents = session.downloadTaskOutput(task_id, file_name, offset,
                                              blocksize)
        offset += len(contents)
        if contents:
            yield contents

    logger.debug('Finished streaming {} from task {}'.format(file_name, task_id))


def tag_koji_build(session, build_id, target, poll_interval=5):
    logger.debug('Finding build tag for target %s', target)
    target_info = session.getBuildTarget(target)
    build_tag = target_info['dest_tag_name']
    logger.info('Tagging build with %s', build_tag)
    task_id = session.tagBuild(build_tag, build_id)

    task = TaskWatcher(session, task_id, poll_interval=poll_interval)
    task.wait()
    if task.failed():
        raise RuntimeError('Task %s failed to tag koji build' % task_id)

    return build_tag

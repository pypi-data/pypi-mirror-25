# -*- coding: utf-8 -*-

import subprocess
from ._base import BaseAction, JobFailed

'''
.. module:: core
   :synopsis: Core actions

.. moduleauthor:: Simon Pirschel <simon@aboutsimon.com>
'''


class Cmd(BaseAction):

    '''Execute shell command

    Example:
        .. code-block:: yaml

            do:
                kind: .core.Cmd
                cmd: python
                args:
                    - hello.py
                cwd: /tmp
                env:
                    SAY: "Hello World."

    Args:
        cmd (str): Command to execute
        args (list, optional): A list of args to pass to command
        cwd (str, optional): Working directory
        env (dict, optional): Dict of environment variables, eg. {"FOO": "BAR"}
        success_exit_code (int): Code process must exist with to be successful,
            default: 0
        raise_on_failure (bool): Raise exception if action failed, default: True
    '''

    def __init__(self, cmd, args=None, cwd=None, env=None, success_exit_code=0,
                 raise_on_failure=True):
        self._cmd = cmd
        self._args = args
        self._cwd = cwd
        self._env = env
        self._success_exit_code = success_exit_code
        self._raise_on_failure = raise_on_failure

        if self._args is not None:
            if type(self._args) is not list:
                self._args = [self._args]
        else:
            self._args = []

    def __call__(self, event, emitter):
        args = [self._cmd] + self._args
        p = subprocess.Popen(args, cwd=self._cwd, env=self._env, shell=True)
        (stdout, stderr) = p.communicate()

        if stdout:
            self._log.info('STDOUT: %s' % (stdout,))

        if stderr:
            self._log.info('STDERR: %s' % (stderr,))

        if p.returncode != self._success_exit_code:
            if self._raise_on_failure is True:
                raise JobFailed(
                    'Cmd %s exited with status code %d' %
                    (' '.join(args), p.returncode)
                )

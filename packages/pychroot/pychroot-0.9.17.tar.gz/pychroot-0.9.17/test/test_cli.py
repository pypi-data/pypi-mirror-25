from __future__ import absolute_import, unicode_literals

import errno
from functools import partial
import os
import shlex
import tempfile
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from pytest import raises

from snakeoil.cli.tool import Tool

from pychroot import __title__ as project
from pychroot.scripts import run
from pychroot.scripts.pychroot import argparser
from pychroot.base import Chroot


def test_arg_parsing():
    """Various argparse checks."""
    pychroot = Tool(argparser)

    # no mounts
    orig_default_mounts = Chroot.default_mounts.copy()
    opts = pychroot.parse_args('--no-mounts fakedir'.split())
    assert Chroot.default_mounts == {}
    Chroot.default_mounts = orig_default_mounts
    assert Chroot.default_mounts != {}

    # single newroot arg with $SHELL from env
    with patch('os.getenv', return_value='shell'):
        opts = pychroot.parse_args(['dir'])
        assert opts.path == 'dir'
        assert opts.command == ['shell', '-i']
        assert opts.mountpoints is None

    # default shell when $SHELL isn't defined in the env
    with patch.dict('os.environ', {}, clear=True):
        opts = pychroot.parse_args(['dir'])
        assert opts.command == ['/bin/sh', '-i']

    # complex args
    opts = pychroot.parse_args(shlex.split(
        '-R /home -B /tmp --ro /var dir cmd arg "arg1 arg2"'))
    assert opts.path == 'dir'
    assert opts.command == ['cmd', 'arg', 'arg1 arg2']
    assert opts.path == 'dir'
    assert opts.mountpoints == {
        '/home': {'recursive': True, 'readonly': False},
        '/tmp': {'recursive': False, 'readonly': False},
        '/var': {'recursive': False, 'readonly': True},
    }


def test_cli(capfd):
    """Various command line interaction checks."""
    pychroot = Tool(argparser)

    # no args
    ret = pychroot([])
    assert ret == 2
    out, err = capfd.readouterr()
    assert err.startswith("pychroot: error: ")

    # nonexistent directory
    ret = pychroot(['nonexistent'])
    assert ret == 1
    out, err = capfd.readouterr()
    assert err == (
        "pychroot: error: cannot change root directory "
        "to 'nonexistent': Not a directory\n")

    with patch('pychroot.scripts.pychroot.Chroot'), \
            patch('os.execvp') as execvp:
        # TODO: replace with tempfile.TemporaryDirectory() context manager
        # after dropping py2.7 support
        chroot = tempfile.mkdtemp()

        # exec arg testing
        pychroot([chroot])
        shell = os.getenv('SHELL', '/bin/sh')
        execvp.assert_called_once_with(shell, [shell, '-i'])
        execvp.reset_mock()

        pychroot([chroot, 'ls -R /'])
        execvp.assert_called_once_with('ls -R /', ['ls -R /'])
        execvp.reset_mock()

        e = EnvironmentError("command doesn't exist")
        e.errno = errno.ENOENT
        e.strerror = os.strerror(e.errno)
        execvp.side_effect = e
        pychroot([chroot, 'nonexistent'])
        out, err = capfd.readouterr()
        assert err == (
            "pychroot: error: failed to run command "
            "'nonexistent': {}\n".format(e.strerror))
        execvp.reset_mock()

        os.rmdir(chroot)


def test_script_run(capfd):
    """Test regular code path for running scripts."""
    script = partial(run, project)

    with patch('{}.scripts.import_module'.format(project)) as import_module:
        import_module.side_effect = ImportError("baz module doesn't exist")

        # default error path when script import fails
        with patch('sys.argv', []):
            with raises(SystemExit) as excinfo:
                script()
            assert excinfo.value.code == 1
            out, err = capfd.readouterr()
            err = err.strip().split('\n')
            assert len(err) == 3
            assert err[0] == "Failed importing: baz module doesn't exist!"
            assert err[1].startswith("Verify that {} and its deps".format(project))
            assert err[2] == "Add --debug to the commandline for a traceback."

        # running with --debug should raise an ImportError when there are issues
        with patch('sys.argv', ['script', '--debug']):
            with raises(ImportError):
                script()
            out, err = capfd.readouterr()
            err = err.strip().split('\n')
            assert len(err) == 2
            assert err[0] == "Failed importing: baz module doesn't exist!"
            assert err[1].startswith("Verify that {} and its deps".format(project))

        import_module.reset_mock()

    # no args
    with patch('sys.argv', []):
        with raises(SystemExit) as excinfo:
            script()
        assert excinfo.value.code == 2
        out, err = capfd.readouterr()
        assert err.startswith("{}: error: ".format(project))

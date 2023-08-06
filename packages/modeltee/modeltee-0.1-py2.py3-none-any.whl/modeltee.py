"""A framework for automating software releases"""

__version__ = "0.1"

from argparse import ArgumentParser
import os
import re
import shutil
from subprocess import run, PIPE
import sys

class Component:
    def __set_name__(self, owner, name):
        components = getattr(owner, '_cls_components', [])
        components.append(self)

    def check_prereqs(self):
        "May be implemented in subclass"
        pass

    def user_confirm(self):
        "May be implemented in subclass"
        pass

class Command(Component):
    """Wrapper for a named command

    Checks that the command exists as a prerequisite.
    """
    def __init__(self, cmd):
        self.cmd = cmd

    def check_prereqs(self):
        found = (shutil.which(self.cmd) is not None)
        yield ('%s command' % self.cmd, found)

    def __call__(self, *args, capture=False, check=True):
        stdout = stderr = (PIPE if capture else None)
        return run([self.cmd] + list(args), check=check, stdout=stdout, stderr=stderr)

class Bumpversion(Command):
    """Wrapper around bumpversion

    See https://github.com/peritus/bumpversion
    """
    def __init__(self, config_file='.bumpversion.cfg'):
        self.config_file = config_file
        super().__init__('bumpversion')

    def __call__(self, *args, capture=False, check=True):
        args = ['--config-file', self.config_file] + list(args)
        return super().__call__(*args, capture=capture, check=check)

    def user_confirm(self):
        out = self('--dry-run', '--allow-dirty', '--list', 'minor', capture=True)
        match = re.search(r"^current_version=(.*)$",
                          out.stdout.decode('utf-8', 'replace'),
                          flags=re.MULTILINE)
        if match:
            print('Version (before changing):', match.group(1))

class Git(Command):
    """Wrapper around the git VCS"""
    def __init__(self):
        super().__init__('git')
        self.repo_root = None

        try:
            res = self('rev-parse', '--show-toplevel', capture=True, check=False)
            if res.returncode == 0:
                self.repo_root = os.fsdecode(res.stdout.strip())
        except FileNotFoundError:
            pass  # This will be flagged by check_prereqs, which hasn't run yet

    def check_prereqs(self):
        yield from super().check_prereqs()
        yield 'git repository', (self.repo_root is not None)

    def user_confirm(self):
        with open(os.path.join(self.repo_root, '.git', 'HEAD')) as f:
            m = re.match(r'ref: refs/heads/(.*)', f.read().strip())
        if m:
            print("On git branch:", m.group(1))

        res = self('log', '-n', '1', '--format=format:%h\x1f%cr\x1f%s',
                           capture=True)
        shorthash, reltime, message = res.stdout.decode('utf-8').split('\x1f', 2)
        print('Last commit ({}):'.format(reltime))
        print(' ', shorthash, message)

def prompt_yn(message):
    message += ' [yn]'
    while True:
        resp = input(message).lower()[:1]
        if resp == 'y':
            return True
        elif resp == 'n':
            return False

ansi_codes = {
    'reset': '\x1b[0m',
    'bold': '\x1b[1m',
    'red': '\x1b[31m',
    'green': '\x1b[32m',
}
def ansi(s, attr):
    return ansi_codes[attr] + str(s) + ansi_codes['reset']

class ReleaserBase:
    _cls_components = []
    
    def __init__(self, version):
        self.version = version

    def check_prereqs(self):
        for obj in self._cls_components:
            yield from obj.check_prereqs()

    def _do_check(self):
        print('Checking prerequisites...')
        all_ok = True
        for descr, ok in self.check_prereqs():
            if ok:
                msg = ansi('OK', 'green')
            else:
                msg = ansi('NOT FOUND', 'red')
                all_ok = False
            print(descr, ':', msg)
        print()
        return all_ok

    def user_confirm(self):
        for obj in self._cls_components:
            obj.user_confirm()
        print("About to release version", ansi(self.version, 'bold'))
        print()
        return prompt_yn('Continue?')

    def before_release(self):
        pass
        
    def do_release(self):
        raise NotImplementedError("Should be implemented in subclass")

    def after_release(self):
        pass

    def release_process(self):
        if not self._do_check():
            print("Prerequisites missing - aborting.")
            sys.exit(1)

        if not self.user_confirm():
            print("User aborted.")
            sys.exit(1)
        
        self.before_release()
        self.do_release()
        self.after_release()

    @classmethod
    def build_arg_parser(cls):
        ap = ArgumentParser()
        ap.add_argument('version',
                        help="The version number for the new release")
        return ap

    @classmethod
    def main(cls, argv=None):
        args = cls.build_arg_parser().parse_args(argv)
        cls(args.version).release_process()


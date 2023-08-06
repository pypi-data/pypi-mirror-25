#!/usr/bin/env python3
"""This is the code to release Modeltee itself"""

from modeltee import ReleaserBase, Command, Bumpversion, Git

class Releaser(ReleaserBase):
    git = Git()
    flit = Command('flit')
    bumpversion = Bumpversion()

    def before_release(self):
        self.bumpversion('--new-version', self.version, 'minor')
        self.flit('build')
        self.git('commit', '-am', 'version number -> {}'.format(self.version))
        self.git('push')

    def do_release(self):
        self.flit('publish')
        self.git('tag', str(self.version))
        self.git('push', '--tags')

if __name__ == '__main__':
    Releaser.main()

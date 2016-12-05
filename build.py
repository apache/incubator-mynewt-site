#!/usr/bin/env python

import os
import click
import sh
from git import Repo, Git
from mkdocs import config
import fileinput

@click.command()
@click.option('-s', '--site-branch', default='master', help='Use this branch as source for the top level pages')
@click.option('-t', '--test-build', is_flag=True, help='Test the build using only the working directory (good for testing for broken links)')
def build(site_branch, test_build):
    if test_build:
        buildForTest()
    else:
        buildForReal(site_branch)

def buildForReal(site_branch):
    # make sure there are no local mods outstanding
    repo = Repo(os.getcwd())
    if repo.is_dirty() or repo.untracked_files:
        print "ERROR: Your working directory has outstanding changes."
        print "Commit or stash them."
        return

    mygit = Git(os.getcwd())
    cfg = config.load_config()

    # sanity check that the version branches exist as named
    for version in cfg['extra']['versions']:
        print 'Verifying branch %s' % (version['branch'])
        mygit.checkout(version['branch'])

    # sanity check - only one latest
    latest = False
    for version in cfg['extra']['versions']:
        if not latest and version['latest']:
            print 'Latest is %s' % (version['branch'])
            latest = True
        elif latest and version['latest']:
            print 'ERROR: More than one version is latest.'
            print 'Only one version can be latest: True.'
            print 'Check mkdocs.yml.'
            return

    mygit.checkout(site_branch)
    print "Building site pages from: %s..." % (site_branch)
    sh.rm('-rf', 'site')
    sh.mkdocs('build', '--clean')

    for version in cfg['extra']['versions']:
        sh.git('checkout', version['branch'], '--', 'docs', 'mkdocs.yml')
        deployVersion(version)

def buildForTest():
    print "Building site pages..."
    updateConfigVersion('develop')
    sh.rm('-rf', 'site')
    sh.mkdocs('build', '--clean')
    sh.git('checkout', '--', 'mkdocs.yml')

    cfg = config.load_config()
    for version in cfg['extra']['versions']:
        deployVersion(version)

def deployVersion(version):
    buildTo(version['branch'])
    if version['latest']:
        buildTo('latest')

def buildTo(branch):
    print 'Building doc pages for: %s...' % (branch)
    branchCfg = config.load_config()
    if branchCfg['extra']['version'] != branch:
        updateConfigVersion(branch)
    sh.mkdocs('build', '--site-dir', 'site/%s' % (branch))
    if branchCfg['extra']['version'] != branch:
        sh.git('checkout', '--', 'mkdocs.yml')

def updateConfigVersion(branch):
    updated = False
    for line in fileinput.input('mkdocs.yml', inplace=True):
        line = line.rstrip()
        if line.find("    version:") == 0:
            line = "    version: '%s'" % (branch)
            updated = True
        print line
    assert updated, "Could not fix the version field on %s" % (branch)

if __name__ == '__main__':
    repo = Repo(os.getcwd())
    branch = repo.active_branch
    mygit = Git(os.getcwd())
    try:
        build()
    finally:
        mygit.checkout(branch.name)

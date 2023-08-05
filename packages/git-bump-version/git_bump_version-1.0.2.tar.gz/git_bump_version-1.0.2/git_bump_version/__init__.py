#!/usr/bin/env python
"""
This script detects the last version number based on git branch and most recent
tag. It then creates the next version, generates it as a tag and outputs it to
stdout.
"""

from __future__ import print_function

import argparse
import errno
import os
import re
import sys

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError


class GitRepository(object):
    """
    Helper class for using as well as abstracting GitPython module dependency.
    """

    def __init__(self, directory):
        self._directory = directory
        self._lazy_repo = None

    @property
    def _repo(self):
        if not self._lazy_repo:
            self._lazy_repo = Repo(self._directory)

        return self._lazy_repo

    @property
    def valid(self):
        """
        Checks if the directory is a valid git repository.

        :rtype: bool
        :returns: True if valid git repository
        """
        try:
            self._repo.git.status()
            return True
        except InvalidGitRepositoryError:
            return False

    @property
    def head_commit(self):
        """
        Returns the HEAD commit.

        :rtype: string
        :returns: HEAD commit as a string
        """
        return self._repo.git.rev_parse('HEAD')

    @property
    def branch_name(self):
        """
        Returns the branch name.

        :rtype: string
        :returns: branch name as a string
        """
        return self._repo.git.rev_parse(['--abbrev-ref', 'HEAD'])

    def get_tags(self, commit):
        """
        Retrieves list of tags for specified commit.

        :param commit: this is commit to get the tags for
        :rtype: list
        :returns: list of string tags
        """
        return self._repo.git.tag(['--contains', commit])

    def is_head_tagged(self):
        """
        Checks if the HEAD commit is tagged.

        :rtype: bool
        :returns: True if HEAD is tagged
        """
        if not self.get_tags(self.head_commit):
            return False

        return True

    def find_tag(self, match):
        """
        Searches for a tag.

        :param match: match parameter for git describe for matching tag
        :rtype: (bool, string)
        :returns: (True, latest_tag) if a match is found.
        """
        try:
            return True, self._repo.git.describe(
                ['--tags', '--match={}'.format(match), '--abbrev=0'])
        except GitCommandError:
            # 'no tag found
            return False, None

    def create_local_tag(self, tag, force=False):
        """
        Creates a local tag.

        :param tag: tag to create
        :param force: True to overwrite existing matching tag if one exists
        """
        options = []

        if force:
            options.append('-f')

        options.append(tag)
        self._repo.git.tag(options)

    def create_remote_tag(self, tag, remote="origin"):
        """
        Pushes a local tag to a remote.

        :param tag: tag to push
        :param remote: remote to push the tag to
        """
        self._repo.git.push([remote, tag])


def get_major_minor_from_branch(repo, regex):
    """
    Retrieves major and minor version from branch name

    :param repo: GitRepository to fetch the branch name from
    :param regex: regex to apply with named groups major and minor
    :rtype: (bool, int, int)
    :returns: (True, major, minor) if parsed successfully
    """
    try:
        match = re.search(regex, repo.branch_name)
        major, minor = int(match.group('major')), int(match.group('minor'))
        return True, major, minor
    except AttributeError:
        return False, None, None


def increment_build_number(prefix, version):
    """
    Increment build number given a version string

    :param prefix: prefix prepended to the version string
    :param version: version string
    :rtype: string
    :returns: (True, major, minor) if parsed successfully
    """
    version = version.replace(prefix, "")
    major, minor, build = version.split('.')
    new_version = "{}{}.{}.{}".format(prefix, int(major), int(minor), int(build) + 1)
    return new_version


def add_git_tag(repo, tag):
    """
    Adds git tag; both local and remote.

    :param tag: tag to add
    """
    repo.create_local_tag(tag)
    repo.create_remote_tag(tag)


def main(args=None):
    """
    Application entry point

    :param args: command line arguments
    """
    parser = argparse.ArgumentParser(
        prog='git_bump_version',
        description='Automatically add new version tag to git based on branch and last tag.')
    parser.add_argument(
        '-bp', '--branch_regex',
        default=r'(?P<major>\d+)\.(?P<minor>\d+)$',
        help='Regex to match major and minor versions from branch')
    parser.add_argument(
        '-vp', '--version_prefix',
        default='',
        help='Version prefix (i.e. "v" would make "1.0.0" into "v1.0.0")')
    parser.add_argument(
        '-dt', '--dont_tag',
        action='store_true',
        help='Do not actually tag the repository')

    # 'For testing args is passed in, but when installing this as a package
    # 'the generated code does not pass it args so it will be None
    if args is not None:
        args = parser.parse_args(args)
    else:
        args = parser.parse_args()

    repo = GitRepository(os.getcwd())

    if not repo.valid:
        print('This tool must be run inside a valid Git repository!', file=sys.stderr)
        return errno.EINVAL

    if repo.is_head_tagged():
        print('Head already tagged!', file=sys.stderr)
        return errno.EEXIST

    matched, major, minor = get_major_minor_from_branch(repo, args.branch_regex)

    if not matched:

        print(
            'Could not parse major and minor from branch: "{}" using \
            regex: "{}"'.format(repo.branch_name, args.branch_regex),
            file=sys.stderr)
        return errno.EINVAL

    match = "{}{}.{}.*".format(args.version_prefix, major, minor)
    found, latest_version = repo.find_tag(match)

    if found:
        new_version = increment_build_number(args.version_prefix, latest_version)
    else:
        new_version = "{}{}.{}.0".format(args.version_prefix, major, minor)

    if not args.dont_tag:
        add_git_tag(repo, new_version)

    print(new_version)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

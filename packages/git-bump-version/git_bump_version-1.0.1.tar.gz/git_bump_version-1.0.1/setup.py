from distutils.core import setup
setup(
    name = 'git_bump_version',
    packages = ['git_bump_version'], # this must be the same as the name above
    version = '1.0.1',
    description = 'Automatically bumps version based on last tag and current branch',
    author = 'Nathan Grubb',
    author_email = 'mrnathangrubb@gmail.com',
    url = 'https://github.com/silent-snowman/git_bump_version',
    download_url = 'https://github.com/silent-snowman/git_bump_version/archive/1.0.1.tar.gz',
    keywords = ['git', 'tag', 'version'],
    classifiers = [],
    entry_points={
        'console_scripts' : [
            'git_bump_version = git_bump_version.__init__:main'
        ]},
    install_requires=[
        'GitPython',
    ],
)

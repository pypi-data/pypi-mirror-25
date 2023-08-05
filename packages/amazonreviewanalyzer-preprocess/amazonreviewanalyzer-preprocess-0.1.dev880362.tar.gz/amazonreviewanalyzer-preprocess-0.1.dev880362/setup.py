import os.path
from setuptools import setup


def get_git_dir():
    if os.path.isdir('.git'):
        git_dir = '.git'
    elif os.path.isfile('.git'):
        # .git is a text file, not a directory
        # -> we're probably in a submodule, git dir is defined in .git
        with open('.git') as f:
            file_content = f.read().strip()
        git_dir = file_content.split('gitdir: ')[1]
        return git_dir
    else:
        # .git is neither a file nor a directory
        # -> we're not in a git repo
        git_dir = ''
    return git_dir


git_dir = get_git_dir()
if git_dir == '':
    git_hash = ''
else:
    try:
        with open(os.path.join(git_dir, 'refs', 'heads', 'master')) as f:
            git_hash = f.read().strip()[:7]
    except FileNotFoundError:
        # git dir exists, but not the rest of the path
        # -> initial repo, nothing committed so far
        git_hash = ''


MAJOR_VERSION = '0'
MINOR_VERSION = '1'
# GIT_VERSION = int(git_hash, 16)
DEV_VERSION = '.dev{}'.format(int(git_hash, 16)) if git_hash else ''

VERSION = '{major}.{minor}{dev}'.format(
    major=MAJOR_VERSION, minor=MINOR_VERSION, dev=DEV_VERSION)

PROJECTNAME = 'amazonreviewanalyzer-preprocess'


setup(
    name=PROJECTNAME,
    version=VERSION,
    description='Preprocessing utilities for the package amazonreviewanalyzer',
    author='Simon Liedtke',
    author_email='sliedtke@uni-bremen.de',
    url='https://gitlab.informatik.uni-bremen.de/sliedtke/{}'.format(
        PROJECTNAME),
    packages=[PROJECTNAME.replace('-', '_')],
    install_requires=['nltk'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Text Processing',
    ],
)

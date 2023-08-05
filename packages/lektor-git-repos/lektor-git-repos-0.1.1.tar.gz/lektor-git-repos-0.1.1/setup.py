from setuptools import setup

setup(
    name='lektor-git-repos',
    description='Fetches your Git repos for display in Lektor templates',
    version='0.1.1',
    author=u'Mark Steve Samson',
    author_email='hello@marksteve.com',
    license='MIT',
    py_modules=['lektor_git_repos'],
    install_requires=['requests'],
    entry_points={
        'lektor.plugins': [
            'git-repos = lektor_git_repos:GitReposPlugin',
        ]
    },
    url='https://git.com/marksteve/lektor-git-repos',
)

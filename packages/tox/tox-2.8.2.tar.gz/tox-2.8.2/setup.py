import io
import os
import re
import sys
import setuptools
from setuptools.command.test import test as TestCommand



class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ["-v", "-epy"]
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        tox.cmdline(self.test_args)

def has_environment_marker_support():
    """
    Tests that setuptools has support for PEP-426 environment marker support.

    The first known release to support it is 0.7 (and the earliest on PyPI seems to be 0.7.2
    so we're using that), see: http://pythonhosted.org/setuptools/history.html#id142

    References:

    * https://wheel.readthedocs.org/en/latest/index.html#defining-conditional-dependencies
    * https://www.python.org/dev/peps/pep-0426/#environment-markers
    """
    import pkg_resources
    try:
        return pkg_resources.parse_version(setuptools.__version__) >= pkg_resources.parse_version('0.7.2')
    except Exception as exc:
        sys.stderr.write("Could not test setuptool's version: %s\n" % exc)
        return False


def get_linked_changelog(here, n=5):
    """changelog containing last n releases with links to issues"""
    repo_url = 'https://github.com/tox-dev/tox'
    changelog_url = '%s/blob/master/CHANGELOG' % repo_url
    with io.open(os.path.join(here, 'CHANGELOG'), encoding='utf-8') as f:
        changelog = f.read()
    header_matches = list(re.finditer('^-+$', changelog, re.MULTILINE))
    lines = changelog[:header_matches[n].start()].splitlines()[:-1]
    title = "Changelog (last %s releases - `full changelog <%s>`_)" % (
        n, changelog_url)
    changelog = '\n'.join([title, '=' * len(title), "\n", "\n".join(lines)])
    issue_replacement = r'`#\1 <%s/issues/\1>`_' % repo_url
    for pattern in [r'#(\d+)', r'issue(\d+)']:
        changelog = re.sub(pattern, issue_replacement, changelog)
    pull_replacement = r'`#p\1 <%s/pull/\1>`_' % repo_url
    changelog = re.sub(r'#p(\d+)', pull_replacement, changelog)
    return changelog


def get_long_description():
    here = os.path.abspath('.')
    with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
        return "%s\n\n%s" % (f.read(), get_linked_changelog(here))


def main():
    version = sys.version_info[:2]
    virtualenv_open = ['virtualenv>=1.11.2']
    virtualenv_capped = ['virtualenv>=1.11.2,<14']
    install_requires = ['py>=1.4.17', 'pluggy>=0.3.0,<1.0']
    extras_require = {}
    if has_environment_marker_support():
        extras_require[':python_version=="2.6"'] = ['argparse']
        extras_require[':python_version=="3.2"'] = virtualenv_capped
        extras_require[':python_version!="3.2"'] = virtualenv_open
    else:
        if version < (2, 7):
            install_requires += ['argparse']
        install_requires += (
            virtualenv_capped if version == (3, 2) else virtualenv_open
        )
    setuptools.setup(
        name='tox',
        description='virtualenv-based automation of test activities',
        long_description=get_long_description(),
        url='https://tox.readthedocs.org/',
        use_scm_version=True,
        license='http://opensource.org/licenses/MIT',
        platforms=['unix', 'linux', 'osx', 'cygwin', 'win32'],
        author='holger krekel',
        author_email='holger@merlinux.eu',
        packages=['tox'],
        entry_points={'console_scripts': 'tox=tox:cmdline\ntox-quickstart=tox._quickstart:main'},
        setup_requires=['setuptools_scm'],
        # we use a public tox version to test, see tox.ini's testenv
        # "deps" definition for the required dependencies
        tests_require=['tox'],
        cmdclass={"test": Tox},
        install_requires=install_requires,
        extras_require=extras_require,
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: POSIX',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: MacOS :: MacOS X',
            'Topic :: Software Development :: Testing',
            'Topic :: Software Development :: Libraries',
            'Topic :: Utilities'] + [
            ('Programming Language :: Python :: %s' % x) for x in
                  '2 2.6 2.7 3 3.3 3.4 3.5 3.6'.split()]
    )

if __name__ == '__main__':
    main()

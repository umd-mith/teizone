from setuptools import setup, Command

class PyTest(Command):
    """
    A command to convince setuptools to run pytests.
    """
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import pytest
        pytest.main("test.py")

setup(
    name = 'teizone',
    version = '0.0.2',
    url = 'http://github.com/umd_mith/teizone',
    author = 'Ed Summers',
    author_email = 'ehs@pobox.com',
    py_modules = ['teizone'],
    description = 'Add coordinates to TEI zones.',
    cmdclass = {'test': PyTest},
    tests_require=['pytest'],
    license='MIT License'
)

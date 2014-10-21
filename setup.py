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
    name = 'zoner',
    version = '0.0.1',
    url = 'http://github.com/umd_mith/zoner',
    author = 'Ed Summers',
    author_email = 'ehs@pobox.com',
    py_modules = ['zoner'],
    description = 'Add coordinates to TEI zones.',
    cmdclass = {'test': PyTest},
    tests_require=['pytest']
)

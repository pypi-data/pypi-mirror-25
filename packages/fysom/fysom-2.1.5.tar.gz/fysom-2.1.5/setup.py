#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'fysom',
        version = '2.1.5',
        description = 'pYthOn Finite State Machine',
        long_description = '',
        author = 'Mansour Behabadi, Jake Gordon, Maximilien Riehl, Stefano',
        author_email = 'mansour@oxplot.com, jake@codeincomplete.com, maximilien.riehl@gmail.com, unknown@domain.invalid',
        license = 'MIT',
        url = 'https://github.com/mriehl/fysom',
        scripts = [],
        packages = ['fysom'],
        namespace_packages = [],
        py_modules = [],
        classifiers = [
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Topic :: Scientific/Engineering'
        ],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        keywords = '',
        python_requires = '',
        obsoletes = [],
    )

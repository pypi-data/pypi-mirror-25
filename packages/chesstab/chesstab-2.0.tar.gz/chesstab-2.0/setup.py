# setup.py
# Copyright 2011 Roger Marsh
# Licence: See LICENCE (BSD licence)

from setuptools import setup

if __name__ == '__main__':

    long_description = open('README').read()

    setup(
        name='chesstab',
        version='2.0',
        description='Database for chess games',
        author='Roger Marsh',
        author_email='roger.marsh@solentware.co.uk',
        url='http://www.solentware.co.uk',
        package_dir={'chesstab':''},
        packages=[
            'chesstab',
            'chesstab.core', 'chesstab.basecore', 'chesstab.gui',
            'chesstab.help',
            'chesstab.db', 'chesstab.dpt', 'chesstab.sqlite', 'chesstab.apsw',
            'chesstab.fonts',
            'chesstab.about',
            ],
        package_data={
            'chesstab.about': ['LICENCE', 'CONTACT'],
            'chesstab.fonts': ['*.TTF', '*.zip'],
            'chesstab.help': ['*.rst', '*.html'],
            },
        long_description=long_description,
        license='BSD',
        classifiers=[
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 3.6',
            'Operating System :: OS Independent',
            'Topic :: Games/Entertainment :: Board Games',
            'Intended Audience :: End Users/Desktop',
            'Development Status :: 4 - Beta',
            ],
        install_requires=[
            'basesup==2.0',
            'chessql==1.0',
            'gridsup==1.0',
            'pgn==1.0',
            'rmappsup==1.0',
            'uci==1.0',
            ],
        dependency_links=[
            'http://solentware.co.uk/files/basesup-2.0.tar.gz',
            'http://solentware.co.uk/files/chessql-1.0.tar.gz',
            'http://solentware.co.uk/files/gridsup-1.0.tar.gz',
            'http://solentware.co.uk/files/pgn-1.0.tar.gz',
            'http://solentware.co.uk/files/rmappsup-1.0.tar.gz',
            'http://solentware.co.uk/files/uci-1.0.tar.gz',
            ],
        )

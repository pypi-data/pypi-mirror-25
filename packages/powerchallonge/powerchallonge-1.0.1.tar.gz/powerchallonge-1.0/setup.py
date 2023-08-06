from distutils.core import setup


def read(filename):
    '''Read content from file'''
    return open(filename).read()

setup(
    name='powerchallonge',
    packages=['challonge', 'tests'],
    version='1.0',
    install_requires=[
        "requests"
    ],
    description='challonge.com API client',
    long_description=(read('README.rst')),
    url='https://github.com/m3fh4q/powerchallonge',
    author='m3fh4q',
    author_email='m3fh4q@yandex.com',

    license=read('LICENSE.md'),
    download_url='https://github.com/m3fh4q/powerchallonge/archive/master.zip',
        classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords=['challonge', 'library', 'client', 'powerchallonge'],
)

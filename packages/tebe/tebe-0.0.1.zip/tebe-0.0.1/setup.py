from distutils.core import setup
setup(
    name='tebe',
    version='0.0.1',
    description='Sphinx writer',
    long_description = open("README.rst").read(),
    author='Lukasz Laba',
    author_email='xx@xxx.xx',
    url='https://xxx.xxx',
    packages=['tebe', 'tebe.pycore'],
    package_data = {'': ['*.png', '*.rst']},
    license = 'GNU General Public License (GPL)',
    keywords = 'sphinx, restructuredtext, ',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        ],
    )

import sys
from setuptools import setup

if sys.version_info.major < 3:
    sys.exit('Sorry, this library only supports Python 3')

setup(
    name='svggraph',
    packages=['svggraph'],
    version='0.0.4',
    description='SVG graph rendering library',
    author='Stephen Brown (Little Fish Solutions LTD)',
    author_email='opensource@littlefish.solutions',
    url='https://github.com/stevelittlefish/svggraph',
    download_url='https://github.com/stevelittlefish/svggraph/archive/v0.0.4.tar.gz',
    keywords=['svg', 'graph', 'line', 'bar', 'pie'],
    license='Apache',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'easysvg>=0.2.1',
    ],
)


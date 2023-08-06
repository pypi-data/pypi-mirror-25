
from setuptools import setup

version = '0.3'

setup(
    name='env2conf',
    version=version,
    description='A tool for the config files generation from environment variables',
    author='Shaobo Wu',
    author_email='wushaobo.china@gmail.com',
    platforms='any',
    url='https://github.com/wushaobo/env2conf',
    license='MIT',
    download_url='https://github.com/wushaobo/env2conf/archive/{}.tar.gz'.format(version),
    keywords=['config', 'env'],
    scripts=['env2conf'],
    install_requires=[
        'jinja2>=2.7,<3'
    ],
    classifiers=[
        # How mature is this project? Common values are
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)

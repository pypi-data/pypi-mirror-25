from setuptools import setup, find_packages
from simple_json_log_formatter import __version__, __author__,\
    __author_email__

setup(
    name='simple_json_log_formatter',
    license='MIT',
    version=__version__,
    packages=find_packages(exclude=['tests']),
    url='https://github.com/flaviocpontes/simple_json_log_formatter',
    download_url='https://github.com/flaviocpontes/simple_json_log_formatter/archive/0.4.0.tar.gz',
    author=__author__,
    author_email=__author_email__,
    python_requires='>=3.4',
    keywords='logging json log output formatter',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    test_suite='tests',
    tests_require=['freezegun', 'coverage', 'codecov'],
    extras_require={'dev': ['factory_boy==2.8.1', 'pathlib2==2.1.0',
                            'freezegun==0.3.9', 'coverage', 'codecov']}
)

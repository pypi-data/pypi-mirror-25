from distutils.core import setup
setup(
    name='timezone_logging',
    packages=['timezone_logging'],
    version='0.1',
    description='Logging with timezone',
    author='Knowru, LLC',
    author_email='hello@knowru.com',
    license='MIT',
    url='https://github.com/knowru/timezone_logging',
    download_url='https://github.com/knowru/timezone_logging/archive/0.1.zip',
    keywords='timezone logging',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Bug Tracking',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=['tzlocal']
)
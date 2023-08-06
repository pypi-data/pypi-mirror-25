from setuptools import setup

VERSION = (0, 0, 1)
version = '.'.join(map(str, VERSION))

def readme():
    with open('README.rst') as f:
        return f.read()
setup(
    name='python-brink',
    version=version,
    description='A python wrapper to the brink api',
    long_description=readme(),
    url='https://github.com/Miller-Media/python-brink',
    author='Kevin Carwile',
    author_email='kevin@miller-media.com',
    license='MIT',
    test_suite='nose.collector',
    tests_require=['nose'],
    packages=[
        'brink'
    ],
    install_requires=[
        'requests>=2.7.0',
    ],
    classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
    ],
    zip_safe=False
)
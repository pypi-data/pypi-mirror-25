from setuptools import setup
from ipaddresstools.ipaddresstools import __version__

packages = [
    'ipaddresstools'
]

tests_require = [
    'pytest',
]

setup(
    name='ipaddresstools',
    version=__version__,
    python_requires='~=3.3',
    description='This is a library used to manipulate and verify ipv4 address\'s. ucast and mcast',
    keywords='ipv4 ip multicast unicast network engineer',
    url='https://github.com/btr1975/ipaddresstools',
    author='Benjamin P. Trachtenberg',
    author_email='e_ben_75-python@yahoo.com',
    license='MIT',
    packages=packages,
    include_package_data=True,
    test_suite='pytest',
    tests_require=tests_require,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
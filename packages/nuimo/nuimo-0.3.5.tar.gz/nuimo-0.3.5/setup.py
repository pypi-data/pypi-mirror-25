from setuptools import setup

setup(
    name='nuimo',
    packages=['nuimo'],
    install_requires=['gatt>=0.2.4'],
    version='0.3.5',
    description='Nuimo SDK for Python on Linux',
    keywords='nuimo',
    url='https://github.com/getsenic/nuimo-linux-python',
    download_url='https://github.com/getsenic/nuimo-linux-python/archive/0.3.5.tar.gz',
    author='Senic GmbH',
    author_email='developers@senic.com',
    license='MIT',
    py_modules=['nuimoctl'],
    entry_points={
        'console_scripts': ['nuimoctl = nuimoctl:main']
    }
)

from setuptools import setup, find_packages

def read(fpath):
    with open(fpath, 'r') as f:
        return f.read()

def requirements(fpath):
    return list(filter(bool, read(fpath).split('\n')))

def version(fpath):
    return read(fpath).strip()

setup(
    name = 'weavery',
    version = version('version.txt'),
    author = 'Matt Bodenhamer',
    author_email = 'mbodenhamer@mbodenhamer.com',
    description = 'Provisioning utilities for Fabric',
    long_description = read('README.rst'),
    url = 'https://github.com/mbodenhamer/weavery',
    packages = find_packages(),
    install_requires = requirements('requirements.in'),
    license = 'MIT',
    keywords = ['fabric', 'provision', 'provisioning'],
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities'
    ]
)

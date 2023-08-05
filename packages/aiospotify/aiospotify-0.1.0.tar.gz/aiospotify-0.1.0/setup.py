from setuptools import setup

setup(
    name='aiospotify',
    packages=['aiospotify'],
    version='0.1.0',
    description='Aiospotify is a request-agnostic wrapper for Spotify\'s Web API.',
    license='MIT',
    author='whitespace',
    url='https://github.com/jdr023/aiospotify',
    download_url='https://github.com/jdr023/aiospotify/archive/v0.1.0.tar.gz',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
    ],
    keywords=['aiospotify', 'spotify', 'asyncio', 'aiohttp', 'api', 'library'],
    install_requires=['aiohttp', 'asyncio']
)

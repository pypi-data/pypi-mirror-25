from setuptools import setup

setup(
    name='pymata-aio',
    version='2.18',
    packages=['pymata_aio'],
    install_requires=['pyserial==2.7', 'websockets'],
    url='https://github.com/MrYsLab/pymata-aio/wiki',
    download_url='https://github.com/MrYsLab/pymata-aio',
    license='GNU General Public License v3 (GPLv3)',
    author='Alan Yorinks',
    author_email='MisterYsLab@gmail.com',
    description='A Python Protocol Abstraction Library For Arduino Firmata using Python asyncio',
    keywords=['Firmata', 'Arduino', 'Protocol'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities',
        'Topic :: Education',
        'Topic :: Home Automation',
    ],
)


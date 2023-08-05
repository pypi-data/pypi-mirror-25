from distutils.core import setup
setup(
    name = 'nambaone_bot',
    packages = ['nambaone_bot'],
    version = '0.1',
    description = 'Python nambaone bot',
    author = 'erjanmx',
    author_email = 'erjanmx@gmail.com',
    url = 'https://github.com/erjanmx/python-nambaone-bot',
    download_url = 'https://github.com/erjanmx/python-nambaone-bot/archive/0.1.tar.gz',
    install_requires=[
        'requests',
    ],
    keywords = ['nambaone', 'bot'],
    classifiers = [],
)
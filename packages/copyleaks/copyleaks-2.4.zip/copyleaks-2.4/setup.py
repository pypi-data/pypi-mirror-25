from distutils.core import setup
setup(
    name = 'copyleaks',
    packages = ['copyleaks'],
    version = '2.4',
    description = 'Copyleaks API gives you access to a variety of plagiarism detection technologies to protect your online content. Get the most comprehensive plagiarism report for your content that is easy to use and integrate.',
    author = 'Copyleaks ltd',
    author_email = 'sales@copyleaks.com',
    url = 'https://api.copyleaks.com',
    download_url = 'https://github.com/Copyleaks/Python-Plagiarism-Checker', 
    keywords = ['copyleaks', 'api', 'plagiarism', 'content', 'checker', 'online', 'academic', 'publishers', 'websites'],
    install_requires=[
        'python-dateutil', 'enum34', 'requests'
    ],
    classifiers = [],
)
from setuptools import setup, find_packages

setup(
    name="deeperlib",
    version="0.1.c",
    packages=find_packages(),
    author='yongjunhe',
    author_email='141250047@smail.nju.edu.cn',
    maintainer='yongjunhe',
    maintainer_email='141250047@smail.nju.edu.cn',
    url = 'https://github.com/sfu-db/deeper',
    include_package_data=True,
    platforms = ["all"],
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'pqdict>=1.0.0',
        'requests>=2.18.4',
        'simplejson>=3.11.1',
        'rauth>=0.7.3',
    ]
)


from setuptools import setup


setup(
    name='respack',
    version='1.2',
    description='Quick packaging of python resource files',
    long_description=open('README.md').read(),
    author='TaoJY',
    author_email='taojy123@163.com',
    maintainer='TaoJY',
    maintainer_email='taojy123@163.com',
    license='MIT License',
    py_modules=['respack'],
    include_package_data=True,
    platforms=["all"],
    url='https://github.com/taojy123/respack',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)



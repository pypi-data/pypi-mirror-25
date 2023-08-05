from setuptools import setup
setup(
    name='jssh', 
    version='4.0.7',
    author='jhy',
    description='A GUI software,YOU can use ssh protocol to manage multiple servers,upload files to servers or download files from them',
    long_description='Use ssh to manage multiple servers, you can upload files to servers or download files from them',
    author_email='fnhchaiying@163.com',
    packages=['jssh'],
    #data_files=[('/usr/local/jssh',['jssh/history.data','jssh/jssh.ico'])],
    requires=['paramiko'],
    install_requires=['paramiko'],
    include_package_data=True,
    classifiers=['Programming Language :: Python :: 2.7'],
    zip_safe=False,
    entry_points={
    'console_scripts': [
        'jssh = jssh.jssh:main',
    ],
    },
    )

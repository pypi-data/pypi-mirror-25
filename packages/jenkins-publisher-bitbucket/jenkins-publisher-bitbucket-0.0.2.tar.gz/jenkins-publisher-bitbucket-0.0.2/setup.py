from setuptools import setup

setup(
    name='jenkins-publisher-bitbucket',
    version='0.0.2',
    description='Jenkins Job Builder Bitbucket Notifier',
    url='https://github.com/bobtfish/jenkins-publisher-bitbucket',
    author='Tomas Doran',
    author_email='bobtfish@bobtfish.net',
    license='MIT license',
    install_requires=[],
    entry_points={
        'jenkins_jobs.publishers': [
            'bitbucket = jenkins_publisher_bitbucket.bitbucket:bitbucket_publisher']},
    packages=['jenkins_publisher_bitbucket'],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'])

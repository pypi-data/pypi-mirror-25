from distutils.core import setup

setup(
    name='multi-logger',
    version='0.1',
    packages=['multilogger'],
    url='https://github.com/ahmedrshdy/multi-logger',
    license='proprietary',
    author='Ahmed Roshdy',
    author_email='a.elshalaby@e-tawasol.com',
    description='Multi channel configurable logger',
    classifiers=[
              'Development Status :: 4 - Beta',
              'Intended Audience :: Developers',
              'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
              'Programming Language :: Python :: 3'
          ],
    install_requires=[
        'watchtower>=0.4.1',
        'boto3>=1.4.7'
    ]
)


from distutils.core import setup

setup(
        author='Vincent Lucas',
        author_email='vincent.lucas@gmail.com',
        description='Calendar access via command line',
        download_url='http://pypi.python.org/pypi/memorandum',
        install_requires=['requests', 'vobject'],
        license='GPLv3',
        long_description=open('README.md').read(),
        name='memorandum',
        packages = ['memorandum'],
        url='https://github.com/vincent-lucas/memorandum',
        version='0.1.2dev',
#        scripts=['memorandum.py'],
)
